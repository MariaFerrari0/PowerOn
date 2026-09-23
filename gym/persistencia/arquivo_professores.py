import os
import struct


class ArquivoProfessores:

    FORMATO = "<i100s150s20s?"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO)

    def __init__(self, caminho="dados/professores.dat"):
        self.caminho = caminho
        self._garantir_arquivo()

    def _garantir_arquivo(self):
        pasta = os.path.dirname(self.caminho)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        if not os.path.exists(self.caminho):
            with open(self.caminho, "wb"):
                pass

    def _codificar_texto(self, texto, tamanho):
        dados = str(texto).encode("utf-8")

        if len(dados) > tamanho:
            raise ValueError(
                f"Texto excede o limite de {tamanho} bytes."
            )

        return dados.ljust(tamanho, b"\x00")

    def _decodificar_texto(self, dados):
        return dados.rstrip(b"\x00").decode("utf-8")

    def inserir(self, professor):
        registro = struct.pack(
            self.FORMATO,
            int(professor.codigo_prof),
            self._codificar_texto(professor.nome, 100),
            self._codificar_texto(professor.endereco, 150),
            self._codificar_texto(professor.telefone, 20),
            True
        )

        with open(self.caminho, "ab") as arquivo:
            arquivo.seek(0, os.SEEK_END)

            posicao_byte = arquivo.tell()
            posicao = posicao_byte // self.TAMANHO_REGISTRO

            arquivo.write(registro)

        return posicao

    def buscar(self, posicao):
        from ..modelos.professor import Professor

        if posicao < 0:
            return None

        offset = posicao * self.TAMANHO_REGISTRO

        with open(self.caminho, "rb") as arquivo:
            arquivo.seek(offset)
            dados = arquivo.read(self.TAMANHO_REGISTRO)

        if len(dados) != self.TAMANHO_REGISTRO:
            return None

        codigo_prof, nome, endereco, telefone, ativo = struct.unpack(
            self.FORMATO,
            dados
        )

        if not ativo:
            return None

        return Professor(
            codigo_prof=codigo_prof,
            nome=self._decodificar_texto(nome),
            endereco=self._decodificar_texto(endereco),
            telefone=self._decodificar_texto(telefone)
        )

    def listar_todos(self):
        from ..modelos.professor import Professor

        registros = []

        with open(self.caminho, "rb") as arquivo:
            posicao = 0

            while True:
                dados = arquivo.read(self.TAMANHO_REGISTRO)

                if not dados:
                    break

                if len(dados) != self.TAMANHO_REGISTRO:
                    raise ValueError(
                        "Arquivo professores.dat possui um registro incompleto."
                    )

                codigo_prof, nome, endereco, telefone, ativo = struct.unpack(
                    self.FORMATO,
                    dados
                )

                professor = Professor(
                    codigo_prof=codigo_prof,
                    nome=self._decodificar_texto(nome),
                    endereco=self._decodificar_texto(endereco),
                    telefone=self._decodificar_texto(telefone)
                )

                registros.append(
                    {
                        "posicao": posicao,
                        "ativo": ativo,
                        "dados": professor
                    }
                )

                posicao += 1

        return registros

    def listar(self):
        professores = []

        for registro in self.listar_todos():
            if registro["ativo"]:
                professores.append(registro["dados"])

        return professores

    def atualizar(self, posicao, professor):
        if self.buscar(posicao) is None:
            return False

        registro = struct.pack(
            self.FORMATO,
            int(professor.codigo_prof),
            self._codificar_texto(professor.nome, 100),
            self._codificar_texto(professor.endereco, 150),
            self._codificar_texto(professor.telefone, 20),
            True
        )

        offset = posicao * self.TAMANHO_REGISTRO

        with open(self.caminho, "r+b") as arquivo:
            arquivo.seek(offset)
            arquivo.write(registro)

        return True

    def remover(self, posicao):
        professor = self.buscar(posicao)

        if professor is None:
            return False

        registro = struct.pack(
            self.FORMATO,
            int(professor.codigo_prof),
            self._codificar_texto(professor.nome, 100),
            self._codificar_texto(professor.endereco, 150),
            self._codificar_texto(professor.telefone, 20),
            False
        )

        offset = posicao * self.TAMANHO_REGISTRO

        with open(self.caminho, "r+b") as arquivo:
            arquivo.seek(offset)
            arquivo.write(registro)

        return True