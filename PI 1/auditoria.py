from datetime import datetime 

def registrar(mensagem):
    with open("auditoria.txt", "a") as arquivo:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        arquivo.write(f"[{data_hora}] {mensagem}\n")