class MatriculaService:

    def __init__(
        self,
        arquivo_matriculas,
        indice_matriculas,
        arquivo_alunos,
        indice_alunos,
        arquivo_modalidades,
        indice_modalidades
    ):
        self.arquivo_matriculas = arquivo_matriculas
        self.indice_matriculas = indice_matriculas

        self.arquivo_alunos = arquivo_alunos
        self.indice_alunos = indice_alunos

        self.arquivo_modalidades = arquivo_modalidades
        self.indice_modalidades = indice_modalidades

    def cadastrar(self, matricula):

        # 1. Verifica se a matrícula já existe
        if self.indice_matriculas.buscar(
            matricula.codigo_matr
        ) is not None:
            raise ValueError(
                f"Matrícula com código "
                f"{matricula.codigo_matr} já existe."
            )

        # 2. Verifica se o aluno existe
        no_aluno = self.indice_alunos.buscar(
            matricula.cod_aluno
        )

        if no_aluno is None:
            raise ValueError(
                f"Aluno com código "
                f"{matricula.cod_aluno} não existe."
            )

        # 3. Verifica se a modalidade existe
        no_modalidade = self.indice_modalidades.buscar(
            matricula.cod_modalidade
        )

        if no_modalidade is None:
            raise ValueError(
                f"Modalidade com código "
                f"{matricula.cod_modalidade} não existe."
            )

        # 4. Verifica quantidade de aulas
        if matricula.qtde_aulas <= 0:
            raise ValueError(
                "A quantidade de aulas deve ser maior que zero."
            )

        # 5. Busca a modalidade no arquivo
        modalidade = self.arquivo_modalidades.buscar(
            no_modalidade.posicao
        )

        if modalidade is None:
            raise ValueError(
                "A modalidade encontrada no índice "
                "não está disponível no arquivo."
            )

        # 6. Verifica limite de alunos
        if modalidade.total_alunos >= modalidade.limite_alunos:
            raise ValueError(
                "A modalidade atingiu o limite de alunos."
            )

        # 7. Grava a matrícula
        posicao = self.arquivo_matriculas.inserir(
            matricula
        )

        # 8. Insere no índice
        inserido = self.indice_matriculas.inserir(
            matricula.codigo_matr,
            posicao
        )

        if not inserido:
            raise ValueError(
                "Não foi possível inserir a matrícula no índice."
            )

        # 9. Incrementa o total de alunos
        modalidade.total_alunos += 1

        self.arquivo_modalidades.atualizar(
            no_modalidade.posicao,
            modalidade
        )

        return posicao

    def buscar(self, codigo_matr):

        no = self.indice_matriculas.buscar(
            codigo_matr
        )

        if no is None:
            return None

        return self.arquivo_matriculas.buscar(
            no.posicao
        )

    def listar(self):

        matriculas = []

        for codigo, posicao in self.indice_matriculas.listar():

            matricula = self.arquivo_matriculas.buscar(
                posicao
            )

            if matricula is not None:
                matriculas.append(matricula)

        return matriculas

    def atualizar(self, codigo_matr, matricula):

        # 1. Busca a matrícula atual
        no = self.indice_matriculas.buscar(
            codigo_matr
        )

        if no is None:
            return False

        # 2. O código não pode ser alterado
        if matricula.codigo_matr != codigo_matr:
            raise ValueError(
                "O código da matrícula não pode ser alterado."
            )

        # 3. Quantidade de aulas precisa ser válida
        if matricula.qtde_aulas <= 0:
            raise ValueError(
                "A quantidade de aulas deve ser maior que zero."
            )

        # 4. Verifica se o aluno existe
        no_aluno = self.indice_alunos.buscar(
            matricula.cod_aluno
        )

        if no_aluno is None:
            raise ValueError(
                f"Aluno com código "
                f"{matricula.cod_aluno} não existe."
            )

        # 5. Recupera a matrícula atual do arquivo
        matricula_atual = self.arquivo_matriculas.buscar(
            no.posicao
        )

        if matricula_atual is None:
            return False

        # 6. Verifica se a nova modalidade existe
        no_modalidade_nova = self.indice_modalidades.buscar(
            matricula.cod_modalidade
        )

        if no_modalidade_nova is None:
            raise ValueError(
                f"Modalidade com código "
                f"{matricula.cod_modalidade} não existe."
            )

        # 7. Recupera a nova modalidade
        modalidade_nova = self.arquivo_modalidades.buscar(
            no_modalidade_nova.posicao
        )

        if modalidade_nova is None:
            raise ValueError(
                "A nova modalidade não está disponível."
            )

        # 8. Verifica se houve troca de modalidade
        trocou_modalidade = (
            matricula_atual.cod_modalidade
            != matricula.cod_modalidade
        )

        if trocou_modalidade:

            # 9. Busca a modalidade antiga
            no_modalidade_antiga = self.indice_modalidades.buscar(
                matricula_atual.cod_modalidade
            )

            if no_modalidade_antiga is None:
                raise ValueError(
                    "A modalidade atual da matrícula "
                    "não foi encontrada."
                )

            # 10. Recupera a modalidade antiga
            modalidade_antiga = self.arquivo_modalidades.buscar(
                no_modalidade_antiga.posicao
            )

            if modalidade_antiga is None:
                raise ValueError(
                    "A modalidade atual da matrícula "
                    "não está disponível."
                )

            # 11. Verifica se existe vaga na nova modalidade
            if (
                modalidade_nova.total_alunos
                >= modalidade_nova.limite_alunos
            ):
                raise ValueError(
                    "A nova modalidade atingiu "
                    "o limite de alunos."
                )

            # 12. Remove o aluno da modalidade antiga
            if modalidade_antiga.total_alunos > 0:
                modalidade_antiga.total_alunos -= 1

            self.arquivo_modalidades.atualizar(
                no_modalidade_antiga.posicao,
                modalidade_antiga
            )

            # 13. Adiciona o aluno na nova modalidade
            modalidade_nova.total_alunos += 1

            self.arquivo_modalidades.atualizar(
                no_modalidade_nova.posicao,
                modalidade_nova
            )

        # 14. Atualiza a matrícula no arquivo
        return self.arquivo_matriculas.atualizar(
            no.posicao,
            matricula
        )

    def remover(self, codigo_matr):

        # 1. Busca a matrícula
        no = self.indice_matriculas.buscar(
            codigo_matr
        )

        if no is None:
            return False

        # 2. Recupera a matrícula
        matricula = self.arquivo_matriculas.buscar(
            no.posicao
        )

        if matricula is None:
            return False

        # 3. Busca a modalidade da matrícula
        no_modalidade = self.indice_modalidades.buscar(
            matricula.cod_modalidade
        )

        if no_modalidade is None:
            raise ValueError(
                "A modalidade da matrícula "
                "não foi encontrada."
            )

        # 4. Recupera a modalidade
        modalidade = self.arquivo_modalidades.buscar(
            no_modalidade.posicao
        )

        if modalidade is None:
            raise ValueError(
                "A modalidade da matrícula "
                "não está disponível."
            )

        # 5. Remove a matrícula logicamente
        removido = self.arquivo_matriculas.remover(
            no.posicao
        )

        if not removido:
            return False

        # 6. Remove a matrícula do índice
        removido_indice = self.indice_matriculas.remover(
            codigo_matr
        )

        if not removido_indice:
            return False

        # 7. Atualiza o total de alunos da modalidade
        if modalidade.total_alunos > 0:

            modalidade.total_alunos -= 1

            self.arquivo_modalidades.atualizar(
                no_modalidade.posicao,
                modalidade
            )

        return True