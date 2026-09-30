class FaturamentoService:

    def __init__(
        self,
        arquivo_modalidades,
        indice_modalidades,
        arquivo_matriculas,
        indice_matriculas,
        arquivo_professores,
        indice_professores
    ):
        self.arquivo_modalidades = arquivo_modalidades
        self.indice_modalidades = indice_modalidades

        self.arquivo_matriculas = arquivo_matriculas
        self.indice_matriculas = indice_matriculas

        self.arquivo_professores = arquivo_professores
        self.indice_professores = indice_professores

    def calcular_por_modalidade(self, codigo_modalidade):

        
        no_modalidade = self.indice_modalidades.buscar(
            codigo_modalidade
        )

        if no_modalidade is None:
            raise ValueError(
                f"Modalidade com código "
                f"{codigo_modalidade} não existe."
            )

        
        modalidade = self.arquivo_modalidades.buscar(
            no_modalidade.posicao
        )

        if modalidade is None:
            raise ValueError(
                "A modalidade encontrada no índice "
                "não está disponível no arquivo."
            )

        
        no_professor = self.indice_professores.buscar(
            modalidade.cod_prof
        )

        if no_professor is None:
            raise ValueError(
                f"Professor com código "
                f"{modalidade.cod_prof} não existe."
            )

       
        professor = self.arquivo_professores.buscar(
            no_professor.posicao
        )

        if professor is None:
            raise ValueError(
                "O professor encontrado no índice "
                "não está disponível no arquivo."
            )

       
        total_aulas = 0

        for codigo, posicao in self.indice_matriculas.listar():

            matricula = self.arquivo_matriculas.buscar(
                posicao
            )

            if matricula is None:
                continue

            if matricula.cod_modalidade == codigo_modalidade:
                total_aulas += matricula.qtde_aulas

       
        faturamento = (
            modalidade.valor_aula * total_aulas
        )

       
        return {
            "codigo_modalidade": modalidade.codigo_modalidade,
            "descricao": modalidade.descricao,
            "cod_prof": professor.codigo_prof,
            "nome_professor": professor.nome,
            "valor_aula": modalidade.valor_aula,
            "total_aulas": total_aulas,
            "faturamento": faturamento
        }

    def listar_faturamento(self):

        relatorio = []

        for codigo, posicao in self.indice_modalidades.listar():

            modalidade = self.arquivo_modalidades.buscar(
                posicao
            )

            if modalidade is None:
                continue

            resultado = self.calcular_por_modalidade(
                codigo
            )

            relatorio.append(resultado)

        return relatorio