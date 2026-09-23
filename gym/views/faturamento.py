from django.shortcuts import render

from ..services.inicializacao import faturamento_service


def lista(request):
    relatorio = faturamento_service.listar_faturamento()

    return render(
        request,
        "gym/relatorios/faturamento.html",
        {
            "relatorio": relatorio,
        }
    )