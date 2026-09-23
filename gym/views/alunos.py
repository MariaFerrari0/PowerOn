from datetime import datetime

from django.shortcuts import render, redirect

from ..modelos.aluno import Aluno
from ..services.inicializacao import aluno_service
from ..utils.imc import calcular_imc, diagnosticar_imc


def lista(request):
    alunos = aluno_service.listar()

    for aluno in alunos:
        try:
            data = datetime.strptime(
                aluno.data_nascimento,
                "%Y-%m-%d"
            )

            aluno.data_nascimento = data.strftime("%d/%m/%Y")

        except ValueError:
            pass

    contexto = {
        "alunos": alunos,
    }

    return render(
        request,
        "gym/alunos/lista.html",
        contexto
    )


def cadastrar(request):
    erro = None

    if request.method == "POST":
        try:
            codigo = int(request.POST.get("codigo"))
            nome = request.POST.get("nome", "").strip()
            data_nascimento = request.POST.get(
                "data_nascimento",
                ""
            ).strip()
            peso = float(request.POST.get("peso"))
            altura = float(request.POST.get("altura"))

            if not nome:
                raise ValueError(
                    "O nome do aluno é obrigatório."
                )

            if peso <= 0:
                raise ValueError(
                    "O peso deve ser maior que zero."
                )

            if altura <= 0:
                raise ValueError(
                    "A altura deve ser maior que zero."
                )

            aluno = Aluno(
                codigo=codigo,
                nome=nome,
                data_nascimento=data_nascimento,
                peso=peso,
                altura=altura,
            )

            aluno_service.cadastrar(aluno)

            return redirect("gym:alunos_lista")

        except (ValueError, TypeError) as e:
            erro = str(e)

    return render(
        request,
        "gym/alunos/cadastrar.html",
        {"erro": erro}
    )


def detalhes(request, codigo):
    aluno = aluno_service.buscar(codigo)

    if aluno is None:
        return redirect("gym:alunos_lista")

    imc = calcular_imc(
        aluno.peso,
        aluno.altura
    )

    diagnostico = diagnosticar_imc(imc)

    try:
        data = datetime.strptime(
            aluno.data_nascimento,
            "%Y-%m-%d"
        )

        data_nascimento = data.strftime("%d/%m/%Y")

    except ValueError:
        data_nascimento = aluno.data_nascimento

    contexto = {
        "aluno": aluno,
        "data_nascimento": data_nascimento,
        "imc": imc,
        "diagnostico": diagnostico,
    }

    return render(
        request,
        "gym/alunos/detalhes.html",
        contexto
    )