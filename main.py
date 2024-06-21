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
    # Removes only the CPF digits, ignoring special characters
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    formatted = False
    num_digits = False
    first_validation = False
    second_validation = False

    # Checks the structure of the CPF (111.222.333-44)
    if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        formatted = True

    # Rules for CPF Validation
    if len(numbers) == 11:
        num_digits = True

        first_sum_product = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        first_expected_digit = (first_sum_product * 10 % 11) % 10
        if numbers[9] == first_expected_digit:
            first_validation = True

        second_sum_product = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        second_expected_digit = (second_sum_product * 10 % 11) % 10
        if numbers[10] == second_expected_digit:
            second_validation = True

        if num_digits and formatted and first_validation and second_validation:
            return True
        else:
            return False

    else:
        return False


if __name__ == '__main__':
    sql = '''select nome_associado, data_nascimento, cpf, matricula from associados order by nome_associado'''

    associados = query_db(sql)
    print(associados)


