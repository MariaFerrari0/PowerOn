from django.shortcuts import render, redirect

from ..modelos.professor import Professor
from ..services.inicializacao import professor_service


def lista(request):
    professores = professor_service.listar()

    contexto = {
        "professores": professores,
    }

    return render(
        request,
        "gym/professores/lista.html",
        contexto
    )


def cadastrar(request):
    erro = None

    if request.method == "POST":
        try:
            codigo_prof = int(
                request.POST.get("codigo_prof")
            )

            nome = request.POST.get(
                "nome",
                ""
            ).strip()

            endereco = request.POST.get(
                "endereco",
                ""
            ).strip()

            telefone = request.POST.get(
                "telefone",
                ""
            ).strip()

            if not nome:
                raise ValueError(
                    "O nome do professor é obrigatório."
                )

            if not endereco:
                raise ValueError(
                    "O endereço do professor é obrigatório."
                )

            if not telefone:
                raise ValueError(
                    "O telefone do professor é obrigatório."
                )

            professor = Professor(
                codigo_prof=codigo_prof,
                nome=nome,
                endereco=endereco,
                telefone=telefone,
            )

            professor_service.cadastrar(professor)

            return redirect(
                "gym:professores_lista"
            )

        except (ValueError, TypeError) as e:
            erro = str(e)

    return render(
        request,
        "gym/professores/cadastrar.html",
        {"erro": erro}
    )


def detalhes(request, codigo_prof):
    professor = professor_service.buscar(codigo_prof)

    if professor is None:
        return redirect(
            "gym:professores_lista"
        )

    contexto = {
        "professor": professor,
    }

    return render(
        request,
        "gym/professores/detalhes.html",
        contexto
    )


def editar(request, codigo_prof):
    professor = professor_service.buscar(codigo_prof)

    if professor is None:
        return redirect(
            "gym:professores_lista"
        )

    erro = None

    if request.method == "POST":
        try:
            nome = request.POST.get(
                "nome",
                ""
            ).strip()

            endereco = request.POST.get(
                "endereco",
                ""
            ).strip()

            telefone = request.POST.get(
                "telefone",
                ""
            ).strip()

            if not nome:
                raise ValueError(
                    "O nome do professor é obrigatório."
                )

            if not endereco:
                raise ValueError(
                    "O endereço do professor é obrigatório."
                )

            if not telefone:
                raise ValueError(
                    "O telefone do professor é obrigatório."
                )

            professor_atualizado = Professor(
                codigo_prof=codigo_prof,
                nome=nome,
                endereco=endereco,
                telefone=telefone,
            )

            professor_service.atualizar(
                codigo_prof,
                professor_atualizado
            )

            return redirect(
                "gym:professores_detalhes",
                codigo_prof=codigo_prof
            )

        except (ValueError, TypeError) as e:
            erro = str(e)

    contexto = {
        "professor": professor,
        "erro": erro,
    }

    return render(
        request,
        "gym/professores/editar.html",
        contexto
    )


def excluir(request, codigo_prof):
    professor = professor_service.buscar(codigo_prof)

    if professor is None:
        return redirect(
            "gym:professores_lista"
        )

    if request.method == "POST":
        try:
            professor_service.remover(codigo_prof)

            return redirect(
                "gym:professores_lista"
            )

        except ValueError as e:
            erro = str(e)

            return render(
                request,
                "gym/professores/confirmar_exclusao.html",
                {
                    "professor": professor,
                    "erro": erro,
                }
            )

    return render(
        request,
        "gym/professores/confirmar_exclusao.html",
        {
            "professor": professor,
        }
    )