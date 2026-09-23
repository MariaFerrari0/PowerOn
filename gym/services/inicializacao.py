from ..persistencia.arquivo_alunos import ArquivoAlunos
from ..persistencia.arquivo_professores import ArquivoProfessores
from ..persistencia.arquivo_modalidades import ArquivoModalidades
from ..persistencia.arquivo_matriculas import ArquivoMatriculas

from ..indices.indice_alunos import IndiceAlunos
from ..indices.indice_professores import IndiceProfessores
from ..indices.indice_modalidades import IndiceModalidades
from ..indices.indice_matriculas import IndiceMatriculas

from .aluno_service import AlunoService
from .professor_service import ProfessorService
from .modalidade_service import ModalidadeService
from .matricula_service import MatriculaService
from .faturamento_service import FaturamentoService


# =========================
# ARQUIVOS
# =========================

arquivo_alunos = ArquivoAlunos()
arquivo_professores = ArquivoProfessores()
arquivo_modalidades = ArquivoModalidades()
arquivo_matriculas = ArquivoMatriculas()


# =========================
# ÍNDICES
# =========================

indice_alunos = IndiceAlunos(arquivo_alunos)
indice_professores = IndiceProfessores(arquivo_professores)
indice_modalidades = IndiceModalidades(arquivo_modalidades)
indice_matriculas = IndiceMatriculas(arquivo_matriculas)


# =========================
# SERVICES
# =========================

aluno_service = AlunoService(
    arquivo_alunos,
    indice_alunos,
    arquivo_matriculas,
    indice_matriculas
)

professor_service = ProfessorService(
    arquivo_professores,
    indice_professores,
    arquivo_modalidades,
    indice_modalidades
)

modalidade_service = ModalidadeService(
    arquivo_modalidades,
    indice_modalidades,
    indice_professores
)

matricula_service = MatriculaService(
    arquivo_matriculas,
    indice_matriculas,
    arquivo_alunos,
    indice_alunos,
    arquivo_modalidades,
    indice_modalidades
)

faturamento_service = FaturamentoService(
    arquivo_modalidades,
    indice_modalidades,
    arquivo_matriculas,
    indice_matriculas,
    arquivo_professores,
    indice_professores
)