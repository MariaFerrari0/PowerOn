from ..estruturas.arvore_binaria import ArvoreBinaria


class IndiceAlunos:

    def __init__(self, arquivo_alunos):
        self.arvore = ArvoreBinaria()
        self.arquivo_alunos = arquivo_alunos

        self.reconstruir()


    def reconstruir(self):
        self.arvore = ArvoreBinaria()

        registros = self.arquivo_alunos.listar_todos()

        for posicao, registro in enumerate(registros):

            
            if not registro["ativo"]:
                continue

            aluno = registro["dados"]

            inserido = self.arvore.inserir(
                aluno.codigo,
                posicao
            )

           
            if not inserido:
                raise ValueError(
                    f"Código de aluno duplicado no arquivo: "
                    f"{aluno.codigo}"
                )


    def inserir(self, codigo, posicao):

        return self.arvore.inserir(
            codigo,
            posicao
        )



    def buscar(self, codigo):
        return self.arvore.buscar(codigo)


    def remover(self, codigo):
        return self.arvore.remover(codigo)

    def listar(self):
        return self.arvore.em_ordem()