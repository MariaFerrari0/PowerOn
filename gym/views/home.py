from django.shortcuts import render

from ..services.inicializacao import (
    aluno_service,
    professor_service,
    modalidade_service,
    matricula_service,
)


def index(request):
    alunos = aluno_service.listar()
    professores = professor_service.listar()
    modalidades = modalidade_service.listar()
    matriculas = matricula_service.listar()

    contexto = {
        "total_alunos": len(alunos),
        "total_professores": len(professores),
        "total_modalidades": len(modalidades),
        "total_matriculas": len(matriculas),
    }

    return render(
        request,
        "gym/home/index.html",
        contexto
    )