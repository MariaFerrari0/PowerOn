class AlunoService:

    def __init__(self, arquivo_alunos, indice_alunos):
        self.arquivo_alunos = arquivo_alunos
        self.indice_alunos = indice_alunos

    # =========================================================
    # CADASTRAR
    # =========================================================

    def cadastrar(self, aluno):
        """
        Cadastra um novo aluno.

        O código não pode existir no índice.
        """

        # Verifica se o código já existe
        existente = self.indice_alunos.buscar(
            aluno.codigo
        )

        if existente is not None:
            raise ValueError(
                f"Aluno com código "
                f"{aluno.codigo} já existe."
            )

        # Grava no arquivo
        posicao = self.arquivo_alunos.inserir(
            aluno
        )

        # Insere no índice
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

        # O código não deve mudar durante a atualização
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
        Realiza a remoção lógica do aluno no arquivo
        e remove sua chave da árvore.
        """

        no = self.indice_alunos.buscar(
            codigo
        )

        if no is None:
            return False

        posicao = no.posicao

        # Primeiro remove logicamente do arquivo
        removido = self.arquivo_alunos.remover(
            posicao
        )

        if not removido:
            return False

        # Depois remove do índice
        removido_indice = self.indice_alunos.remover(
            codigo
        )

        if not removido_indice:
            return False

        return True