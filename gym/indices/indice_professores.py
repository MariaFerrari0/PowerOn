from ..estruturas.arvore_binaria import ArvoreBinaria


class IndiceProfessores:

    def __init__(self, arquivo_professores):
        self.arvore = ArvoreBinaria()
        self.arquivo_professores = arquivo_professores

        self.reconstruir()

    def reconstruir(self):
        self.arvore = ArvoreBinaria()

        registros = self.arquivo_professores.listar_todos()

        for registro in registros:
            if not registro["ativo"]:
                continue

            professor = registro["dados"]
            posicao = registro["posicao"]

            inserido = self.arvore.inserir(
                professor.codigo_prof,
                posicao
            )

            if not inserido:
                raise ValueError(
                    f"Código de professor duplicado no arquivo: "
                    f"{professor.codigo_prof}"
                )

    def inserir(self, codigo_prof, posicao):
        return self.arvore.inserir(
            codigo_prof,
            posicao
        )

    def buscar(self, codigo_prof):
        return self.arvore.buscar(codigo_prof)

    def remover(self, codigo_prof):
        return self.arvore.remover(codigo_prof)

    def listar(self):
        return self.arvore.em_ordem()