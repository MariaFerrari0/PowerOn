from django.shortcuts import render, redirect

from ..modelos.modalidade import Modalidade
from ..services.inicializacao import modalidade_service
from ..services.inicializacao import professor_service


def lista(request):
    modalidades = modalidade_service.listar()
    professores = professor_service.listar()

    professores_dict = {
        professor.codigo_prof: professor.nome
        for professor in professores
    }

    for modalidade in modalidades:
        modalidade.nome_professor = professores_dict.get(
            modalidade.cod_prof,
            "Professor não encontrado"
        )

    contexto = {
        "modalidades": modalidades,
    }

    return render(
        request,
        "gym/modalidades/lista.html",
        contexto
    )


def cadastrar(request):
    erro = None
    professores = professor_service.listar()

    if request.method == "POST":
        try:
            codigo_modalidade = int(
                request.POST.get("codigo_modalidade")
            )

            descricao = request.POST.get(
                "descricao",
                ""
            ).strip()

            cod_prof = int(
                request.POST.get("cod_prof")
            )

            valor_aula = float(
                request.POST.get("valor_aula")
            )

            limite_alunos = int(
                request.POST.get("limite_alunos")
            )

            if not descricao:
                raise ValueError(
                    "A descrição da modalidade é obrigatória."
                )

            if valor_aula <= 0:
                raise ValueError(
                    "O valor da aula deve ser maior que zero."
                )

            if limite_alunos <= 0:
                raise ValueError(
                    "O limite de alunos deve ser maior que zero."
                )

            modalidade = Modalidade(
                codigo_modalidade=codigo_modalidade,
                descricao=descricao,
                cod_prof=cod_prof,
                valor_aula=valor_aula,
                limite_alunos=limite_alunos,
                total_alunos=0,
            )

            modalidade_service.cadastrar(modalidade)

            return redirect(
                "gym:modalidades_lista"
            )

        except (ValueError, TypeError) as e:
            erro = str(e)

    contexto = {
        "erro": erro,
        "professores": professores,
    }

    return render(
        request,
        "gym/modalidades/cadastrar.html",
        contexto
    )


def detalhes(request, codigo_modalidade):
    modalidade = modalidade_service.buscar(
        codigo_modalidade
    )

    if modalidade is None:
        return redirect(
            "gym:modalidades_lista"
        )

    professor = professor_service.buscar(
        modalidade.cod_prof
    )

    if professor is not None:
        modalidade.nome_professor = professor.nome
    else:
        modalidade.nome_professor = "Professor não encontrado"

    contexto = {
        "modalidade": modalidade,
    }

    return render(
        request,
        "gym/modalidades/detalhes.html",
        contexto
    )


def editar(request, codigo_modalidade):
    modalidade = modalidade_service.buscar(
        codigo_modalidade
    )

    if modalidade is None:
        return redirect(
            "gym:modalidades_lista"
        )

    professores = professor_service.listar()
    erro = None

    if request.method == "POST":
        try:
            descricao = request.POST.get(
                "descricao",
                ""
            ).strip()

            cod_prof = int(
                request.POST.get("cod_prof")
            )

            valor_aula = float(
                request.POST.get("valor_aula")
            )

            limite_alunos = int(
                request.POST.get("limite_alunos")
            )

            if not descricao:
                raise ValueError(
                    "A descrição da modalidade é obrigatória."
                )

            if valor_aula <= 0:
                raise ValueError(
                    "O valor da aula deve ser maior que zero."
                )

            if limite_alunos <= 0:
                raise ValueError(
                    "O limite de alunos deve ser maior que zero."
                )

            modalidade_atualizada = Modalidade(
                codigo_modalidade=codigo_modalidade,
                descricao=descricao,
                cod_prof=cod_prof,
                valor_aula=valor_aula,
                limite_alunos=limite_alunos,
                total_alunos=modalidade.total_alunos,
            )

            modalidade_service.atualizar(
                codigo_modalidade,
                modalidade_atualizada
            )

            return redirect(
                "gym:modalidades_detalhes",
                codigo_modalidade=codigo_modalidade
            )

        except (ValueError, TypeError) as e:
            erro = str(e)

    contexto = {
        "modalidade": modalidade,
        "professores": professores,
        "erro": erro,
    }

    return render(
        request,
        "gym/modalidades/editar.html",
        contexto
    )


def excluir(request, codigo_modalidade):
    modalidade = modalidade_service.buscar(
        codigo_modalidade
    )

    if modalidade is None:
        return redirect(
            "gym:modalidades_lista"
        )

    professor = professor_service.buscar(
        modalidade.cod_prof
    )

    if professor is not None:
        modalidade.nome_professor = professor.nome
    else:
        modalidade.nome_professor = "Professor não encontrado"

    if request.method == "POST":
        try:
            modalidade_service.remover(
                codigo_modalidade
            )

            return redirect(
                "gym:modalidades_lista"
            )

        except ValueError as e:
            erro = str(e)

            return render(
                request,
                "gym/modalidades/confirmar_exclusao.html",
                {
                    "modalidade": modalidade,
                    "erro": erro,
                }
            )

    return render(
        request,
        "gym/modalidades/confirmar_exclusao.html",
        {
            "modalidade": modalidade,
        }
    )