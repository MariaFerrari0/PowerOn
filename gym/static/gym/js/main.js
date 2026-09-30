

document.addEventListener("DOMContentLoaded", () => {

    inicializarMensagens();
    inicializarConfirmacoes();
    inicializarMenuMobile();

});

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

function inicializarMenuMobile() {

    const botaoMenu =
        document.getElementById("menu-mobile");


    const sidebar =
        document.querySelector(".sidebar");


    const overlay =
        document.getElementById(
            "sidebar-overlay"
        );


    if (
        !botaoMenu ||
        !sidebar ||
        !overlay
    ) {

        return;

    }


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


 
    overlay.addEventListener(
        "click",
        () => {

            fecharMenu();

        }
    );


   

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