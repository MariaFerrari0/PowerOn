from ..estruturas.arvore_binaria import ArvoreBinaria


class IndiceModalidades:

    def __init__(self, arquivo_modalidades):
        self.arvore = ArvoreBinaria()
        self.arquivo_modalidades = arquivo_modalidades

        self.reconstruir()

    def reconstruir(self):
        self.arvore = ArvoreBinaria()

        registros = self.arquivo_modalidades.listar_todos()

        for registro in registros:
            if not registro["ativo"]:
                continue

            modalidade = registro["dados"]
            posicao = registro["posicao"]

            inserido = self.arvore.inserir(
                modalidade.codigo_modalidade,
                posicao
            )

            if not inserido:
                raise ValueError(
                    f"Código de modalidade duplicado no arquivo: "
                    f"{modalidade.codigo_modalidade}"
                )

    def inserir(self, codigo_modalidade, posicao):
        return self.arvore.inserir(
            codigo_modalidade,
            posicao
        )

    def buscar(self, codigo_modalidade):
        return self.arvore.buscar(
            codigo_modalidade
        )

    def remover(self, codigo_modalidade):
        return self.arvore.remover(
            codigo_modalidade
        )

    def listar(self):
        return self.arvore.em_ordem()