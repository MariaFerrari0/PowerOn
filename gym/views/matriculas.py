from django.shortcuts import render, redirect

from ..modelos.matricula import Matricula
from ..services.inicializacao import matricula_service
from ..services.inicializacao import aluno_service
from ..services.inicializacao import modalidade_service


def lista(request):
    matriculas = matricula_service.listar()

    alunos = aluno_service.listar()
    modalidades = modalidade_service.listar()

    alunos_dict = {
        aluno.codigo: aluno.nome
        for aluno in alunos
    }

    modalidades_dict = {
        modalidade.codigo_modalidade: modalidade.descricao
        for modalidade in modalidades
    }

    for matricula in matriculas:
        matricula.nome_aluno = alunos_dict.get(
            matricula.cod_aluno,
            "Aluno não encontrado"
        )

        matricula.descricao_modalidade = modalidades_dict.get(
            matricula.cod_modalidade,
            "Modalidade não encontrada"
        )

    contexto = {
        "matriculas": matriculas,
    }

    return render(
        request,
        "gym/matriculas/lista.html",
        contexto
    )


def cadastrar(request):
    erro = None

    alunos = aluno_service.listar()
    modalidades = modalidade_service.listar()

    if request.method == "POST":
        try:
            codigo_matr = int(
                request.POST.get("codigo_matr")
            )

            cod_aluno = int(
                request.POST.get("cod_aluno")
            )

            cod_modalidade = int(
                request.POST.get("cod_modalidade")
            )

            qtde_aulas = int(
                request.POST.get("qtde_aulas")
            )

            if qtde_aulas <= 0:
                raise ValueError(
                    "A quantidade de aulas deve ser maior que zero."
                )

            matricula = Matricula(
                codigo_matr=codigo_matr,
                cod_aluno=cod_aluno,
                cod_modalidade=cod_modalidade,
                qtde_aulas=qtde_aulas,
            )

            matricula_service.cadastrar(
                matricula
            )

            return redirect(
                "gym:matriculas_lista"
            )

        except (ValueError, TypeError) as e:
            erro = str(e)

    contexto = {
        "erro": erro,
        "alunos": alunos,
        "modalidades": modalidades,
    }

    return render(
        request,
        "gym/matriculas/cadastrar.html",
        contexto
    )


def detalhes(request, codigo_matr):
    matricula = matricula_service.buscar(
        codigo_matr
    )

    if matricula is None:
        return redirect(
            "gym:matriculas_lista"
        )

    aluno = aluno_service.buscar(
        matricula.cod_aluno
    )

    modalidade = modalidade_service.buscar(
        matricula.cod_modalidade
    )

    if aluno is not None:
        matricula.nome_aluno = aluno.nome
    else:
        matricula.nome_aluno = "Aluno não encontrado"

    if modalidade is not None:
        matricula.descricao_modalidade = modalidade.descricao
    else:
        matricula.descricao_modalidade = "Modalidade não encontrada"

    contexto = {
        "matricula": matricula,
    }

    return render(
        request,
        "gym/matriculas/detalhes.html",
        contexto
    )


def excluir(request, codigo_matr):
    matricula = matricula_service.buscar(
        codigo_matr
    )

    if matricula is None:
        return redirect(
            "gym:matriculas_lista"
        )

    aluno = aluno_service.buscar(
        matricula.cod_aluno
    )

    modalidade = modalidade_service.buscar(
        matricula.cod_modalidade
    )

    if aluno is not None:
        matricula.nome_aluno = aluno.nome
    else:
        matricula.nome_aluno = "Aluno não encontrado"

    if modalidade is not None:
        matricula.descricao_modalidade = modalidade.descricao
    else:
        matricula.descricao_modalidade = "Modalidade não encontrada"

    erro = None

    if request.method == "POST":
        try:
            matricula_service.remover(
                codigo_matr
            )

            return redirect(
                "gym:matriculas_lista"
            )

        except ValueError as e:
            erro = str(e)

    contexto = {
        "matricula": matricula,
        "erro": erro,
    }

    return render(
        request,
        "gym/matriculas/confirmar_exclusao.html",
        contexto
    )


def editar(request, codigo_matr):
    matricula = matricula_service.buscar(
        codigo_matr
    )

    if matricula is None:
        return redirect(
            "gym:matriculas_lista"
        )

    alunos = aluno_service.listar()
    modalidades = modalidade_service.listar()

    erro = None

    if request.method == "POST":
        try:
            cod_aluno = int(
                request.POST.get("cod_aluno")
            )

            cod_modalidade = int(
                request.POST.get("cod_modalidade")
            )

            qtde_aulas = int(
                request.POST.get("qtde_aulas")
            )

            if qtde_aulas <= 0:
                raise ValueError(
                    "A quantidade de aulas deve ser maior que zero."
                )

            matricula_atualizada = Matricula(
                codigo_matr=codigo_matr,
                cod_aluno=cod_aluno,
                cod_modalidade=cod_modalidade,
                qtde_aulas=qtde_aulas,
            )

            matricula_service.atualizar(
                codigo_matr,
                matricula_atualizada
            )

            return redirect(
                "gym:matriculas_detalhes",
                codigo_matr=codigo_matr
            )

        except (ValueError, TypeError) as e:
            erro = str(e)

    aluno = aluno_service.buscar(
        matricula.cod_aluno
    )

    modalidade = modalidade_service.buscar(
        matricula.cod_modalidade
    )

    if aluno is not None:
        matricula.nome_aluno = aluno.nome
    else:
        matricula.nome_aluno = "Aluno não encontrado"

    if modalidade is not None:
        matricula.descricao_modalidade = modalidade.descricao
    else:
        matricula.descricao_modalidade = "Modalidade não encontrada"

    contexto = {
        "matricula": matricula,
        "alunos": alunos,
        "modalidades": modalidades,
        "erro": erro,
    }

    return render(
        request,
        "gym/matriculas/editar.html",
        contexto
    )