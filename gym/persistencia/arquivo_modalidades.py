import os
import struct


class ArquivoModalidades:

    FORMATO = "<i100sifii?"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO)

    def __init__(self, caminho="dados/modalidades.dat"):
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

    def inserir(self, modalidade):
        registro = struct.pack(
            self.FORMATO,
            int(modalidade.codigo_modalidade),
            self._codificar_texto(
                modalidade.descricao,
                100
            ),
            int(modalidade.cod_prof),
            float(modalidade.valor_aula),
            int(modalidade.limite_alunos),
            int(modalidade.total_alunos),
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

    def buscar(self, posicao):
        from ..modelos.modalidade import Modalidade

        if posicao < 0:
            return None

        offset = (
            posicao * self.TAMANHO_REGISTRO
        )

        with open(self.caminho, "rb") as arquivo:
            arquivo.seek(offset)

            dados = arquivo.read(
                self.TAMANHO_REGISTRO
            )

        if len(dados) != self.TAMANHO_REGISTRO:
            return None

        (
            codigo_modalidade,
            descricao,
            cod_prof,
            valor_aula,
            limite_alunos,
            total_alunos,
            ativo
        ) = struct.unpack(
            self.FORMATO,
            dados
        )

        if not ativo:
            return None

        return Modalidade(
            codigo_modalidade=codigo_modalidade,
            descricao=self._decodificar_texto(
                descricao
            ),
            cod_prof=cod_prof,
            valor_aula=valor_aula,
            limite_alunos=limite_alunos,
            total_alunos=total_alunos
        )

    def listar_todos(self):
        from ..modelos.modalidade import Modalidade

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
                        "Arquivo modalidades.dat possui "
                        "um registro incompleto."
                    )

                (
                    codigo_modalidade,
                    descricao,
                    cod_prof,
                    valor_aula,
                    limite_alunos,
                    total_alunos,
                    ativo
                ) = struct.unpack(
                    self.FORMATO,
                    dados
                )

                modalidade = Modalidade(
                    codigo_modalidade=codigo_modalidade,
                    descricao=self._decodificar_texto(
                        descricao
                    ),
                    cod_prof=cod_prof,
                    valor_aula=valor_aula,
                    limite_alunos=limite_alunos,
                    total_alunos=total_alunos
                )

                registros.append(
                    {
                        "posicao": posicao,
                        "ativo": ativo,
                        "dados": modalidade
                    }
                )

                posicao += 1

        return registros

    def listar(self):
        modalidades = []

        for registro in self.listar_todos():

            if registro["ativo"]:
                modalidades.append(
                    registro["dados"]
                )

        return modalidades

    def atualizar(self, posicao, modalidade):
        if self.buscar(posicao) is None:
            return False

        registro = struct.pack(
            self.FORMATO,
            int(modalidade.codigo_modalidade),
            self._codificar_texto(
                modalidade.descricao,
                100
            ),
            int(modalidade.cod_prof),
            float(modalidade.valor_aula),
            int(modalidade.limite_alunos),
            int(modalidade.total_alunos),
            True
        )

        offset = (
            posicao * self.TAMANHO_REGISTRO
        )

        with open(self.caminho, "r+b") as arquivo:
            arquivo.seek(offset)
            arquivo.write(registro)

        return True

    def remover(self, posicao):
        modalidade = self.buscar(posicao)

        if modalidade is None:
            return False

        registro = struct.pack(
            self.FORMATO,
            int(modalidade.codigo_modalidade),
            self._codificar_texto(
                modalidade.descricao,
                100
            ),
            int(modalidade.cod_prof),
            float(modalidade.valor_aula),
            int(modalidade.limite_alunos),
            int(modalidade.total_alunos),
            False
        )

        offset = (
            posicao * self.TAMANHO_REGISTRO
        )

        with open(self.caminho, "r+b") as arquivo:
            arquivo.seek(offset)
            arquivo.write(registro)

        return True