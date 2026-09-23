from ..estruturas.arvore_binaria import ArvoreBinaria


class IndiceAlunos:

    def __init__(self, arquivo_alunos):
        self.arvore = ArvoreBinaria()
        self.arquivo_alunos = arquivo_alunos

        self.reconstruir()

    # =========================================================
    # RECONSTRUÇÃO DO ÍNDICE
    # =========================================================

    def reconstruir(self):
        """
        Reconstrói a árvore binária utilizando os registros
        ativos existentes no arquivo alunos.dat.
        """

        # Cria uma árvore nova
        self.arvore = ArvoreBinaria()

        registros = self.arquivo_alunos.listar_todos()

        for posicao, registro in enumerate(registros):

            # Ignora registros removidos logicamente
            if not registro["ativo"]:
                continue

            aluno = registro["dados"]

            inserido = self.arvore.inserir(
                aluno.codigo,
                posicao
            )

            # Verifica código duplicado
            if not inserido:
                raise ValueError(
                    f"Código de aluno duplicado no arquivo: "
                    f"{aluno.codigo}"
                )

    # =========================================================
    # INSERÇÃO
    # =========================================================

    def inserir(self, codigo, posicao):
        """
        Insere o código e a posição do aluno no índice.
        """

        return self.arvore.inserir(
            codigo,
            posicao
        )

    # =========================================================
    # BUSCA
    # =========================================================

    def buscar(self, codigo):
        """
        Busca um aluno pelo código.

        Retorna o nó encontrado ou None.
        """

        return self.arvore.buscar(codigo)

    # =========================================================
    # REMOÇÃO
    # =========================================================

    def remover(self, codigo):
        """
        Remove o código do aluno da árvore.
        """

        return self.arvore.remover(codigo)

    # =========================================================
    # LISTAGEM
    # =========================================================

    def listar(self):
        """
        Retorna os códigos e posições existentes
        no índice, em ordem crescente.
        """

        return self.arvore.em_ordem()