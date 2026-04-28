import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lobo2404$",
        database="sistema_votacao"
    )

    cursor = conn.cursor(dictionary=True)

except mysql.connector.Error as err:
    print("Erro ao conectar no banco:", err)