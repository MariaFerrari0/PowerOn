from django.urls import path
from .views import home, alunos, professores, modalidades, matriculas

app_name = "gym"

urlpatterns = [
    path("", home.index, name="home"),
    path("alunos/", alunos.lista, name="alunos_lista"),
    path("alunos/cadastrar/", alunos.cadastrar, name="alunos_cadastrar"),
    path("alunos/<int:codigo>/", alunos.detalhes, name="alunos_detalhes"),
    path("alunos/<int:codigo>/editar/", alunos.editar, name="alunos_editar"),
    path("alunos/<int:codigo>/excluir/", alunos.excluir, name="alunos_excluir"),

      path("professores/", professores.lista, name="professores_lista"),
    path("professores/cadastrar/", professores.cadastrar, name="professores_cadastrar"),
    path("professores/<int:codigo_prof>/", professores.detalhes, name="professores_detalhes"),
    path("professores/<int:codigo_prof>/editar/", professores.editar, name="professores_editar"),
    path("professores/<int:codigo_prof>/excluir/", professores.excluir, name="professores_excluir"),

   # MODALIDADES
   path("modalidades/", modalidades.lista, name="modalidades_lista"),
   path("modalidades/cadastrar/", modalidades.cadastrar, name="modalidades_cadastrar"),
   path("modalidades/<int:codigo_modalidade>/", modalidades.detalhes, name="modalidades_detalhes"),
   path("modalidades/<int:codigo_modalidade>/editar/", modalidades.editar, name="modalidades_editar"),
   path("modalidades/<int:codigo_modalidade>/excluir/", modalidades.excluir, name="modalidades_excluir"),

   # MATRÍCULAS
   path("matriculas/", matriculas.lista, name="matriculas_lista"),
   path("matriculas/cadastrar/", matriculas.cadastrar, name="matriculas_cadastrar"),
   path("matriculas/<int:codigo_matr>/", matriculas.detalhes, name="matriculas_detalhes"),
   path("matriculas/<int:codigo_matr>/excluir/", matriculas.excluir, name="matriculas_excluir"),

  
    


]