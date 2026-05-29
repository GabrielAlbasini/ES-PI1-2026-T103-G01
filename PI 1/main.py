from menus import menu_principal
from auditoria import registrar


# INICIAR SISTEMA

if __name__ == "__main__":

    # Registra abertura do sistema
    registrar(
        "Sistema iniciado"
    )

    menu_principal()