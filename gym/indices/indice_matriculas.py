from ..estruturas.arvore_binaria import ArvoreBinaria


class IndiceMatriculas:

    def __init__(self, arquivo_matriculas):
        self.arvore = ArvoreBinaria()
        self.arquivo_matriculas = arquivo_matriculas

        self.reconstruir()

    def reconstruir(self):
        self.arvore = ArvoreBinaria()

        registros = self.arquivo_matriculas.listar_todos()

        for registro in registros:
            if not registro["ativo"]:
                continue

            matricula = registro["dados"]
            posicao = registro["posicao"]

            inserido = self.arvore.inserir(
                matricula.codigo_matr,
                posicao
            )

            if not inserido:
                raise ValueError(
                    f"Código de matrícula duplicado no arquivo: "
                    f"{matricula.codigo_matr}"
                )

    def inserir(self, codigo_matr, posicao):
        return self.arvore.inserir(
            codigo_matr,
            posicao
        )

    def buscar(self, codigo_matr):
        return self.arvore.buscar(
            codigo_matr
        )

    def remover(self, codigo_matr):
        return self.arvore.remover(
            codigo_matr
        )

    def listar(self):
        return self.arvore.em_ordem()