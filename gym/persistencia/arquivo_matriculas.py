import os
import struct


class ArquivoMatriculas:

    FORMATO = "<iiii?"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO)

    def __init__(self, caminho="dados/matriculas.dat"):
        self.caminho = caminho
        self._garantir_arquivo()

    def _garantir_arquivo(self):
        pasta = os.path.dirname(self.caminho)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        if not os.path.exists(self.caminho):
            with open(self.caminho, "wb"):
                pass

    def inserir(self, matricula):
        registro = struct.pack(
            self.FORMATO,
            int(matricula.codigo_matr),
            int(matricula.cod_aluno),
            int(matricula.cod_modalidade),
            int(matricula.qtde_aulas),
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
        from ..modelos.matricula import Matricula

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
            codigo_matr,
            cod_aluno,
            cod_modalidade,
            qtde_aulas,
            ativo
        ) = struct.unpack(
            self.FORMATO,
            dados
        )

        if not ativo:
            return None

        return Matricula(
            codigo_matr=codigo_matr,
            cod_aluno=cod_aluno,
            cod_modalidade=cod_modalidade,
            qtde_aulas=qtde_aulas
        )

    def listar_todos(self):
        from ..modelos.matricula import Matricula

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
                        "Arquivo matriculas.dat possui "
                        "um registro incompleto."
                    )

                (
                    codigo_matr,
                    cod_aluno,
                    cod_modalidade,
                    qtde_aulas,
                    ativo
                ) = struct.unpack(
                    self.FORMATO,
                    dados
                )

                matricula = Matricula(
                    codigo_matr=codigo_matr,
                    cod_aluno=cod_aluno,
                    cod_modalidade=cod_modalidade,
                    qtde_aulas=qtde_aulas
                )

                registros.append(
                    {
                        "posicao": posicao,
                        "ativo": ativo,
                        "dados": matricula
                    }
                )

                posicao += 1

        return registros

    def listar(self):
        matriculas = []

        for registro in self.listar_todos():

            if registro["ativo"]:
                matriculas.append(
                    registro["dados"]
                )

        return matriculas

    def atualizar(self, posicao, matricula):
        if self.buscar(posicao) is None:
            return False

        registro = struct.pack(
            self.FORMATO,
            int(matricula.codigo_matr),
            int(matricula.cod_aluno),
            int(matricula.cod_modalidade),
            int(matricula.qtde_aulas),
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
        matricula = self.buscar(posicao)

        if matricula is None:
            return False

        registro = struct.pack(
            self.FORMATO,
            int(matricula.codigo_matr),
            int(matricula.cod_aluno),
            int(matricula.cod_modalidade),
            int(matricula.qtde_aulas),
            False
        )

        offset = (
            posicao * self.TAMANHO_REGISTRO
        )

        with open(self.caminho, "r+b") as arquivo:
            arquivo.seek(offset)
            arquivo.write(registro)

        return True