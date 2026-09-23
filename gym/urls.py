from django.urls import path
from .views import home, alunos

app_name = "gym"

urlpatterns = [
    path("", home.index, name="home"),
    path("alunos/", alunos.lista, name="alunos_lista"),
    path("alunos/cadastrar/", alunos.cadastrar, name="alunos_cadastrar"),
    path("alunos/<int:codigo>/", alunos.detalhes, name="alunos_detalhes"),
]