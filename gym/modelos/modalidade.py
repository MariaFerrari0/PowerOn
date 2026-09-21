class Modalidade:
    def __init__(
        self,
        codigo_modalidade,
        descricao,
        cod_prof,
        valor_aula,
        limite_alunos,
        total_alunos=0
    ):
        self.codigo_modalidade = codigo_modalidade
        self.descricao = descricao
        self.cod_prof = cod_prof
        self.valor_aula = valor_aula
        self.limite_alunos = limite_alunos
        self.total_alunos = total_alunos