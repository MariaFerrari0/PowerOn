from django.urls import path
from .views import home, alunos, professores

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
]