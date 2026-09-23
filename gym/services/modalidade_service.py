class ModalidadeService:

    def __init__(
        self,
        arquivo_modalidades,
        indice_modalidades,
        indice_professores
    ):
        self.arquivo_modalidades = arquivo_modalidades
        self.indice_modalidades = indice_modalidades
        self.indice_professores = indice_professores

    def cadastrar(self, modalidade):
        # Verifica se a modalidade já existe
        if self.indice_modalidades.buscar(
            modalidade.codigo_modalidade
        ) is not None:
            raise ValueError(
                f"Modalidade com código "
                f"{modalidade.codigo_modalidade} já existe."
            )

        # Verifica se o professor existe
        professor = self.indice_professores.buscar(
            modalidade.cod_prof
        )

        if professor is None:
            raise ValueError(
                f"Professor com código "
                f"{modalidade.cod_prof} não existe."
            )

        # Valida o limite de alunos
        if modalidade.limite_alunos <= 0:
            raise ValueError(
                "O limite de alunos deve ser maior que zero."
            )

        # O cadastro começa sem alunos
        modalidade.total_alunos = 0

        # Grava no arquivo físico
        posicao = self.arquivo_modalidades.inserir(
            modalidade
        )

        # Cria o índice código -> posição
        inserido = self.indice_modalidades.inserir(
            modalidade.codigo_modalidade,
            posicao
        )

        if not inserido:
            raise ValueError(
                "Não foi possível inserir a modalidade no índice."
            )

        return posicao

    def buscar(self, codigo_modalidade):
        no = self.indice_modalidades.buscar(
            codigo_modalidade
        )

        if no is None:
            return None

        return self.arquivo_modalidades.buscar(
            no.posicao
        )

    def listar(self):
        modalidades = []

        for codigo, posicao in self.indice_modalidades.listar():

            modalidade = self.arquivo_modalidades.buscar(
                posicao
            )

            if modalidade is not None:
                modalidades.append(modalidade)

        return modalidades

    def atualizar(
        self,
        codigo_modalidade,
        modalidade
    ):
        no = self.indice_modalidades.buscar(
            codigo_modalidade
        )

        if no is None:
            return False

        if modalidade.codigo_modalidade != codigo_modalidade:
            raise ValueError(
                "O código da modalidade não pode ser alterado."
            )

        # Verifica se o novo professor existe
        professor = self.indice_professores.buscar(
            modalidade.cod_prof
        )

        if professor is None:
            raise ValueError(
                f"Professor com código "
                f"{modalidade.cod_prof} não existe."
            )

        if modalidade.limite_alunos <= 0:
            raise ValueError(
                "O limite de alunos deve ser maior que zero."
            )

        # Não permite reduzir o limite abaixo
        # da quantidade atual de alunos
        if modalidade.limite_alunos < modalidade.total_alunos:
            raise ValueError(
                "O limite de alunos não pode ser menor "
                "que o total atual de alunos."
            )

        return self.arquivo_modalidades.atualizar(
            no.posicao,
            modalidade
        )

    def remover(self, codigo_modalidade):
        no = self.indice_modalidades.buscar(
            codigo_modalidade
        )

        if no is None:
            return False

        modalidade = self.arquivo_modalidades.buscar(
            no.posicao
        )

        if modalidade is None:
            return False

        # Não permite excluir modalidade
        # que possui alunos matriculados
        if modalidade.total_alunos > 0:
            raise ValueError(
                "Não é possível remover uma modalidade "
                "que possui alunos matriculados."
            )

        removido = self.arquivo_modalidades.remover(
            no.posicao
        )

        if not removido:
            return False

        removido_indice = self.indice_modalidades.remover(
            codigo_modalidade
        )

        if not removido_indice:
            return False

        return True