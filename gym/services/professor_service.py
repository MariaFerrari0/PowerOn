class ProfessorService:

    def __init__(self, arquivo_professores, indice_professores):
        self.arquivo_professores = arquivo_professores
        self.indice_professores = indice_professores

    def cadastrar(self, professor):
        if self.indice_professores.buscar(
            professor.codigo_prof
        ) is not None:
            raise ValueError(
                f"Professor com código "
                f"{professor.codigo_prof} já existe."
            )

        posicao = self.arquivo_professores.inserir(professor)

        inserido = self.indice_professores.inserir(
            professor.codigo_prof,
            posicao
        )

        if not inserido:
            raise ValueError(
                "Não foi possível inserir o professor no índice."
            )

        return posicao

    def buscar(self, codigo_prof):
        no = self.indice_professores.buscar(codigo_prof)

        if no is None:
            return None

        return self.arquivo_professores.buscar(
            no.posicao
        )

    def listar(self):
        professores = []

        for codigo, posicao in self.indice_professores.listar():

            professor = self.arquivo_professores.buscar(
                posicao
            )

            if professor is not None:
                professores.append(professor)

        return professores

    def atualizar(self, codigo_prof, professor):
        no = self.indice_professores.buscar(codigo_prof)

        if no is None:
            return False

        if professor.codigo_prof != codigo_prof:
            raise ValueError(
                "O código do professor não pode ser alterado."
            )

        return self.arquivo_professores.atualizar(
            no.posicao,
            professor
        )

    def remover(self, codigo_prof):
        no = self.indice_professores.buscar(codigo_prof)

        if no is None:
            return False

        posicao = no.posicao

        removido = self.arquivo_professores.remover(
            posicao
        )

        if not removido:
            return False

        removido_indice = self.indice_professores.remover(
            codigo_prof
        )

        if not removido_indice:
            return False

        return True