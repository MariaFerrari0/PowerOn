class AlunoService:

    def __init__(
        self,
        arquivo_alunos,
        indice_alunos,
        arquivo_matriculas,
        indice_matriculas
    ):
        self.arquivo_alunos = arquivo_alunos
        self.indice_alunos = indice_alunos
        self.arquivo_matriculas = arquivo_matriculas
        self.indice_matriculas = indice_matriculas

    # =========================================================
    # CADASTRAR
    # =========================================================

    def cadastrar(self, aluno):
        """
        Cadastra um novo aluno.
        O código não pode existir no índice.
        """

        existente = self.indice_alunos.buscar(
            aluno.codigo
        )

        if existente is not None:
            raise ValueError(
                f"Aluno com código "
                f"{aluno.codigo} já existe."
            )

        posicao = self.arquivo_alunos.inserir(
            aluno
        )

        inserido = self.indice_alunos.inserir(
            aluno.codigo,
            posicao
        )

        if not inserido:
            raise ValueError(
                f"Não foi possível inserir "
                f"o código {aluno.codigo} no índice."
            )

        return posicao

    # =========================================================
    # BUSCAR
    # =========================================================

    def buscar(self, codigo):
        """
        Busca um aluno pelo código.
        """

        no = self.indice_alunos.buscar(
            codigo
        )

        if no is None:
            return None

        return self.arquivo_alunos.buscar(
            no.posicao
        )

    # =========================================================
    # LISTAR
    # =========================================================

    def listar(self):
        """
        Retorna todos os alunos ativos.
        """

        alunos = []

        indices = self.indice_alunos.listar()

        for codigo, posicao in indices:
            aluno = self.arquivo_alunos.buscar(
                posicao
            )

            if aluno is not None:
                alunos.append(aluno)

        return alunos

    # =========================================================
    # ATUALIZAR
    # =========================================================

    def atualizar(self, codigo, aluno):
        """
        Atualiza os dados de um aluno mantendo
        sua posição no arquivo e sua chave no índice.
        """

        no = self.indice_alunos.buscar(
            codigo
        )

        if no is None:
            return False

        if aluno.codigo != codigo:
            raise ValueError(
                "O código do aluno não pode "
                "ser alterado."
            )

        return self.arquivo_alunos.atualizar(
            no.posicao,
            aluno
        )

    # =========================================================
    # REMOVER
    # =========================================================

    def remover(self, codigo):
        """
        Remove um aluno somente se ele não possuir
        matrícula ativa.
        """

        no = self.indice_alunos.buscar(
            codigo
        )

        if no is None:
            return False

        # Verifica se o aluno possui matrícula ativa.
        for codigo_matr, posicao in self.indice_matriculas.listar():
            matricula = self.arquivo_matriculas.buscar(
                posicao
            )

            if matricula is None:
                continue

            if matricula.cod_aluno == codigo:
                raise ValueError(
                    "Não é possível excluir o aluno "
                    "porque ele possui uma matrícula ativa."
                )

        posicao = no.posicao

        # Remove logicamente do arquivo.
        removido = self.arquivo_alunos.remover(
            posicao
        )

        if not removido:
            return False

        # Remove da árvore.
        removido_indice = self.indice_alunos.remover(
            codigo
        )

        if not removido_indice:
            return False

        return True