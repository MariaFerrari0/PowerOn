from .no_arvore import NoArvore


class ArvoreBinaria:
    """
    Árvore Binária de Busca utilizada como estrutura
    de índice em memória.

    Cada nó possui:
        - chave: código utilizado para pesquisa
        - posicao: posição do registro no arquivo
        - esquerda: filho com chave menor
        - direita: filho com chave maior
    """

    def __init__(self):
        self.raiz = None

    # =========================================================
    # INSERÇÃO
    # =========================================================

    def inserir(self, chave, posicao):
        """
        Insere uma nova chave na árvore.

        Retorna True quando a inserção é realizada.
        Retorna False quando a chave já existe.
        """

        novo_no = NoArvore(chave, posicao)

        if self.raiz is None:
            self.raiz = novo_no
            return True

        return self._inserir_recursivo(self.raiz, novo_no)

    def _inserir_recursivo(self, atual, novo_no):

        if novo_no.chave < atual.chave:

            if atual.esquerda is None:
                atual.esquerda = novo_no
                return True

            return self._inserir_recursivo(
                atual.esquerda,
                novo_no
            )

        if novo_no.chave > atual.chave:

            if atual.direita is None:
                atual.direita = novo_no
                return True

            return self._inserir_recursivo(
                atual.direita,
                novo_no
            )

        # A chave já existe.
        return False

    # =========================================================
    # BUSCA
    # =========================================================

    def buscar(self, chave):
        """
        Procura uma chave na árvore.

        Retorna o nó encontrado.
        Retorna None caso a chave não exista.
        """

        atual = self.raiz

        while atual is not None:

            if chave == atual.chave:
                return atual

            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return None

    # =========================================================
    # REMOÇÃO
    # =========================================================

    def remover(self, chave):
        """
        Remove uma chave da árvore.

        Retorna True quando o elemento é removido.
        Retorna False quando a chave não existe.
        """

        self.raiz, removido = self._remover_recursivo(
            self.raiz,
            chave
        )

        return removido

    def _remover_recursivo(self, atual, chave):

        if atual is None:
            return None, False

        # Procurar na esquerda
        if chave < atual.chave:

            atual.esquerda, removido = self._remover_recursivo(
                atual.esquerda,
                chave
            )

            return atual, removido

        # Procurar na direita
        if chave > atual.chave:

            atual.direita, removido = self._remover_recursivo(
                atual.direita,
                chave
            )

            return atual, removido

        # =====================================================
        # ENCONTRAMOS O NÓ
        # =====================================================

        # Caso 1:
        # Nó sem filhos
        if atual.esquerda is None and atual.direita is None:
            return None, True

        # Caso 2:
        # Nó possui somente filho direito
        if atual.esquerda is None:
            return atual.direita, True

        # Caso 2:
        # Nó possui somente filho esquerdo
        if atual.direita is None:
            return atual.esquerda, True

        # =====================================================
        # Caso 3:
        # Nó possui dois filhos
        # =====================================================

        sucessor = self._menor_no(atual.direita)

        atual.chave = sucessor.chave
        atual.posicao = sucessor.posicao

        atual.direita, _ = self._remover_recursivo(
            atual.direita,
            sucessor.chave
        )

        return atual, True

    # =========================================================
    # ENCONTRAR MENOR NÓ
    # =========================================================

    def _menor_no(self, no):

        atual = no

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual

    # =========================================================
    # PERCURSO EM ORDEM
    # =========================================================

    def em_ordem(self):
        """
        Retorna os elementos da árvore em ordem crescente.

        Formato:
            [(chave, posicao), ...]
        """

        resultado = []

        self._em_ordem_recursivo(
            self.raiz,
            resultado
        )

        return resultado

    def _em_ordem_recursivo(self, atual, resultado):

        if atual is None:
            return

        self._em_ordem_recursivo(
            atual.esquerda,
            resultado
        )

        resultado.append(
            (atual.chave, atual.posicao)
        )

        self._em_ordem_recursivo(
            atual.direita,
            resultado
        )

    # =========================================================
    # PERCURSO PRÉ-ORDEM
    # =========================================================

    def pre_ordem(self):
        resultado = []

        self._pre_ordem_recursivo(
            self.raiz,
            resultado
        )

        return resultado

    def _pre_ordem_recursivo(self, atual, resultado):

        if atual is None:
            return

        resultado.append(
            (atual.chave, atual.posicao)
        )

        self._pre_ordem_recursivo(
            atual.esquerda,
            resultado
        )

        self._pre_ordem_recursivo(
            atual.direita,
            resultado
        )

    # =========================================================
    # PERCURSO PÓS-ORDEM
    # =========================================================

    def pos_ordem(self):
        resultado = []

        self._pos_ordem_recursivo(
            self.raiz,
            resultado
        )

        return resultado

    def _pos_ordem_recursivo(self, atual, resultado):

        if atual is None:
            return

        self._pos_ordem_recursivo(
            atual.esquerda,
            resultado
        )

        self._pos_ordem_recursivo(
            atual.direita,
            resultado
        )

        resultado.append(
            (atual.chave, atual.posicao)
        )