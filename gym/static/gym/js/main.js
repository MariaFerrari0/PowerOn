/* =========================================================
   POWERON - JAVASCRIPT
   Interações gerais do sistema
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    inicializarMensagens();
    inicializarConfirmacoes();

});


/* =========================================================
   MENSAGENS
   ========================================================= */

function inicializarMensagens() {

    const mensagens = document.querySelectorAll(
        ".mensagem"
    );

    mensagens.forEach((mensagem) => {

        setTimeout(() => {

            mensagem.style.opacity = "0";

            mensagem.style.transform =
                "translateY(-10px)";

            setTimeout(() => {
                mensagem.remove();
            }, 300);

        }, 5000);

    });

}


/* =========================================================
   CONFIRMAÇÃO DE EXCLUSÃO
   ========================================================= */

function inicializarConfirmacoes() {

    const botoes = document.querySelectorAll(
        "[data-confirmar]"
    );

    botoes.forEach((botao) => {

        botao.addEventListener("click", (event) => {

            const mensagem =
                botao.dataset.confirmar ||
                "Tem certeza que deseja continuar?";

            const confirmado =
                window.confirm(mensagem);

            if (!confirmado) {
                event.preventDefault();
            }

        });

    });

}