import psycopg2 as psycopg2
from dotenv import load_dotenv
import os
import re


def connect_db():
    load_dotenv('.env', override=True)

    isProduction = False

    host = os.getenv('HOST_PRODUCTION') if isProduction else os.getenv('HOST_TEST')
    port = os.getenv('PORT')
    database = os.getenv('DATABASE_PRODUCTION') if isProduction else os.getenv('DATABASE_TEST')
    user = os.getenv('USER_PRODUCTION') if isProduction else os.getenv('USER_TEST')
    password = os.getenv('PASSWORD_PRODUCTION') if isProduction else os.getenv('PASSWORD_TEST')

    connection = psycopg2.connect(host=host,
                                  port=port,
                                  database=database,
                                  user=user,
                                  password=password)

    return connection


def query_db(sql_query):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql_query)
    aux_query = cur.fetchall()
    registers = []
    for rec in aux_query:
        registers.append(rec)
    con.close()

    return registers


def execute_sql(sql, values, return_id=False):
    con = connect_db()
    cur = con.cursor()

    aux_sql = None

    try:
        cur.execute(sql, values)
        if return_id:
            aux_sql = cur.fetchall()
        con.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print('Error: %s' % error)
        con.rollback()
        cur.close()
        return 1

    cur.close()

    if return_id:
        return aux_sql[0][0]


def validator(cpf):
    # Retira apenas os dígitos do CPF, ignorando os caracteres especiais
    numbers = [int(digito) for digito in cpf if digito.isdigit()]

    formatacao = False
    quant_digitos = False
    validacao1 = False
    validacao2 = False

    # Verifica a estrutura do CPF (111.222.333-44)
    if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        formatacao = True

    if len(numeros) == 11:
        quant_digitos = True

        soma_produtos = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
        digito_esperado = (soma_produtos * 10 % 11) % 10
        if numeros[9] == digito_esperado:
            validacao1 = True

        soma_produtos1 = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
        digito_esperado1 = (soma_produtos1 * 10 % 11) % 10
        if numeros[10] == digito_esperado1:
            validacao2 = True

        if quant_digitos == True and formatacao == True and validacao1 == True and validacao2 == True:
            print(f"O CPF {cpf} é válido.")
        else:
            print(f"O CPF {cpf} não é válido... Tente outro CPF...")

    else:
        print(print(f"O CPF {cpf} não é válido... Tente outro CPF..."))

if __name__ == '__main__':
    sql = '''select * from associados'''

    associados = query_db(sql)
