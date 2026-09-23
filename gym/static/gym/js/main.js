/* =========================================================
   POWERON - JAVASCRIPT
   Interações gerais do sistema
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    inicializarMensagens();

    inicializarConfirmacoes();

    inicializarMenuMobile();

});


/* =========================================================
   MENSAGENS
   ========================================================= */

function inicializarMensagens() {

    const mensagens =
        document.querySelectorAll(".mensagem");


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

    const botoes =
        document.querySelectorAll(
            "[data-confirmar]"
        );


    botoes.forEach((botao) => {

        botao.addEventListener(
            "click",
            (event) => {

                const mensagem =
                    botao.dataset.confirmar ||
                    "Tem certeza que deseja continuar?";


                const confirmado =
                    window.confirm(mensagem);


                if (!confirmado) {

                    event.preventDefault();

                }

            }
        );

    });

}


/* =========================================================
   MENU MOBILE
   ========================================================= */

function inicializarMenuMobile() {

    const botaoMenu =
        document.getElementById("menu-mobile");


    const sidebar =
        document.querySelector(".sidebar");


    const overlay =
        document.getElementById(
            "sidebar-overlay"
        );


    /*
     * Se algum elemento não existir,
     * não executa o restante da função.
     */

    if (
        !botaoMenu ||
        !sidebar ||
        !overlay
    ) {

        return;

    }


    /* =====================================================
       ABRIR / FECHAR MENU
       ===================================================== */

    botaoMenu.addEventListener(
        "click",
        () => {

            const aberto =
                sidebar.classList.toggle(
                    "sidebar-aberta"
                );


            overlay.classList.toggle(
                "ativo",
                aberto
            );


            botaoMenu.setAttribute(
                "aria-expanded",
                aberto
            );


            botaoMenu.setAttribute(
                "aria-label",
                aberto
                    ? "Fechar menu"
                    : "Abrir menu"
            );


            botaoMenu.textContent =
                aberto ? "✕" : "☰";

        }
    );


    /* =====================================================
       FECHAR AO CLICAR NO FUNDO
       ===================================================== */

    overlay.addEventListener(
        "click",
        () => {

            fecharMenu();

        }
    );


    /* =====================================================
       FECHAR AO CLICAR EM UM LINK
       ===================================================== */

    const links =
        sidebar.querySelectorAll(
            ".menu-item"
        );


    links.forEach((link) => {

        link.addEventListener(
            "click",
            () => {

                fecharMenu();

            }
        );

    });


    /* =====================================================
       FUNÇÃO PARA FECHAR O MENU
       ===================================================== */

    function fecharMenu() {

        sidebar.classList.remove(
            "sidebar-aberta"
        );


        overlay.classList.remove(
            "ativo"
        );


        botaoMenu.setAttribute(
            "aria-expanded",
            "false"
        );


        botaoMenu.setAttribute(
            "aria-label",
            "Abrir menu"
        );


        botaoMenu.textContent = "☰";

    }

}