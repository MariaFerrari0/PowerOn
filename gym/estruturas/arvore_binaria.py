from .no_arvore import NoArvore


class ArvoreBinaria:

    def __init__(self):
        self.raiz = None

    def inserir(self, chave, posicao):
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

        
        return False

    def buscar(self, chave):

        atual = self.raiz

        while atual is not None:

            if chave == atual.chave:
                return atual

            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return None

    def remover(self, chave):

        self.raiz, removido = self._remover_recursivo(
            self.raiz,
            chave
        )

        return removido

    def _remover_recursivo(self, atual, chave):

        if atual is None:
            return None, False

       
        if chave < atual.chave:

            atual.esquerda, removido = self._remover_recursivo(
                atual.esquerda,
                chave
            )

            return atual, removido

        
        if chave > atual.chave:

            atual.direita, removido = self._remover_recursivo(
                atual.direita,
                chave
            )

            return atual, removido

       
        # Nó sem filhos
        if atual.esquerda is None and atual.direita is None:
            return None, True

        # Nó possui somente filho direito
        if atual.esquerda is None:
            return atual.direita, True

        # Nó possui somente filho esquerdo
        if atual.direita is None:
            return atual.esquerda, True

      
        # Nó possui dois filhos
        sucessor = self._menor_no(atual.direita)

        atual.chave = sucessor.chave
        atual.posicao = sucessor.posicao

        atual.direita, _ = self._remover_recursivo(
            atual.direita,
            sucessor.chave
        )

        return atual, True

    def _menor_no(self, no):

        atual = no

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual

    def em_ordem(self):
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