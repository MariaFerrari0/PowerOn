import os
import struct


class ArquivoAlunos:

    # =========================================================
    # FORMATO DO REGISTRO
    # =========================================================

    # i    -> código (inteiro)
    # 100s -> nome (100 bytes)
    # 10s  -> data de nascimento (10 bytes)
    # f    -> peso (float)
    # f    -> altura (float)
    # ?    -> ativo (booleano)

    FORMATO = "<i100s10sff?"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO)

    def __init__(self, caminho="dados/alunos.dat"):
        self.caminho = caminho
        self._garantir_arquivo()

    # =========================================================
    # PREPARAÇÃO DO ARQUIVO
    # =========================================================

    def _garantir_arquivo(self):
        pasta = os.path.dirname(self.caminho)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        if not os.path.exists(self.caminho):
            with open(self.caminho, "wb"):
                pass

    # =========================================================
    # CONVERSÃO DE TEXTO
    # =========================================================

    def _codificar_texto(self, texto, tamanho):
        """
        Converte uma string para bytes de tamanho fixo.
        """

        dados = texto.encode("utf-8")

        if len(dados) > tamanho:
            raise ValueError(
                f"Texto excede o limite de {tamanho} bytes."
            )

        return dados.ljust(tamanho, b"\x00")

    def _decodificar_texto(self, dados):
        """
        Converte bytes de tamanho fixo novamente para string.
        """

        return dados.rstrip(b"\x00").decode("utf-8")

    # =========================================================
    # INSERÇÃO
    # =========================================================

    def inserir(self, aluno):
        """
        Insere um aluno no final do arquivo.

        Retorna a posição lógica do registro.
        """

        nome = self._codificar_texto(
            aluno.nome,
            100
        )

        data_nascimento = self._codificar_texto(
            aluno.data_nascimento,
            10
        )

        registro = struct.pack(
            self.FORMATO,
            int(aluno.codigo),
            nome,
            data_nascimento,
            float(aluno.peso),
            float(aluno.altura),
            True
        )

        with open(self.caminho, "ab") as arquivo:

            arquivo.seek(0, os.SEEK_END)

            posicao_byte = arquivo.tell()

            posicao = (
                posicao_byte // self.TAMANHO_REGISTRO
            )

            arquivo.write(registro)

        return posicao

    # =========================================================
    # BUSCA
    # =========================================================

    def buscar(self, posicao):
        """
        Busca um aluno pela posição lógica do registro.
        """

        from ..modelos.aluno import Aluno

        if posicao < 0:
            return None

        offset = posicao * self.TAMANHO_REGISTRO

        with open(self.caminho, "rb") as arquivo:

            arquivo.seek(offset)

            dados = arquivo.read(
                self.TAMANHO_REGISTRO
            )

        if len(dados) != self.TAMANHO_REGISTRO:
            return None

        (
            codigo,
            nome,
            data_nascimento,
            peso,
            altura,
            ativo
        ) = struct.unpack(
            self.FORMATO,
            dados
        )

        if not ativo:
            return None

        return Aluno(
            codigo=codigo,
            nome=self._decodificar_texto(nome),
            data_nascimento=self._decodificar_texto(
                data_nascimento
            ),
            peso=peso,
            altura=altura
        )

    # =========================================================
    # LISTAR TODOS OS REGISTROS
    # =========================================================

    def listar_todos(self):
        """
        Retorna todos os registros, inclusive os inativos.

        Cada item possui:
            posicao
            ativo
            dados
        """

        from ..modelos.aluno import Aluno

        registros = []

        with open(self.caminho, "rb") as arquivo:

            posicao = 0

            while True:

                dados = arquivo.read(
                    self.TAMANHO_REGISTRO
                )

                if not dados:
                    break

                if len(dados) != self.TAMANHO_REGISTRO:
                    raise ValueError(
                        "Arquivo alunos.dat possui "
                        "um registro incompleto."
                    )

                (
                    codigo,
                    nome,
                    data_nascimento,
                    peso,
                    altura,
                    ativo
                ) = struct.unpack(
                    self.FORMATO,
                    dados
                )

                aluno = Aluno(
                    codigo=codigo,
                    nome=self._decodificar_texto(nome),
                    data_nascimento=self._decodificar_texto(
                        data_nascimento
                    ),
                    peso=peso,
                    altura=altura
                )

                registros.append(
                    {
                        "posicao": posicao,
                        "ativo": ativo,
                        "dados": aluno
                    }
                )

                posicao += 1

        return registros

    # =========================================================
    # LISTAR SOMENTE ATIVOS
    # =========================================================

    def listar(self):
        """
        Retorna somente os alunos ativos.
        """

        alunos = []

        for registro in self.listar_todos():

            if registro["ativo"]:
                alunos.append(
                    registro["dados"]
                )

        return alunos

    # =========================================================
    # ATUALIZAÇÃO
    # =========================================================

    def atualizar(self, posicao, aluno):
        """
        Atualiza o registro mantendo a mesma posição.
        """

        if self.buscar(posicao) is None:
            return False

        nome = self._codificar_texto(
            aluno.nome,
            100
        )

        data_nascimento = self._codificar_texto(
            aluno.data_nascimento,
            10
        )

        registro = struct.pack(
            self.FORMATO,
            int(aluno.codigo),
            nome,
            data_nascimento,
            float(aluno.peso),
            float(aluno.altura),
            True
        )

        offset = posicao * self.TAMANHO_REGISTRO

        with open(self.caminho, "r+b") as arquivo:

            arquivo.seek(offset)
            arquivo.write(registro)

        return True

    # =========================================================
    # REMOÇÃO LÓGICA
    # =========================================================

    def remover(self, posicao):
        """
        Marca o registro como inativo sem removê-lo
        fisicamente do arquivo.
        """

        aluno = self.buscar(posicao)

        if aluno is None:
            return False

        nome = self._codificar_texto(
            aluno.nome,
            100
        )

        data_nascimento = self._codificar_texto(
            aluno.data_nascimento,
            10
        )

        registro = struct.pack(
            self.FORMATO,
            int(aluno.codigo),
            nome,
            data_nascimento,
            float(aluno.peso),
            float(aluno.altura),
            False
        )

        offset = posicao * self.TAMANHO_REGISTRO

        with open(self.caminho, "r+b") as arquivo:

            arquivo.seek(offset)
            arquivo.write(registro)

        return True