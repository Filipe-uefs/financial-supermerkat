from usecases.connect import connect
from config.config import load_config


def create_tables():

    config = load_config()
    conn = connect(config)
    cursor = conn.cursor()

    sql_insert_table_account_payable = '''CREATE TABLE IF NOT EXISTS "account_payable" (
          "id" SERIAL PRIMARY KEY,
          "unit_value" float8,
          "due_date" timestamp,
          "description" varchar,
          "type_id" integer
        ) '''

    sql_insert_table_account_type = '''CREATE TABLE IF NOT EXISTS "type" (
                                "id" SERIAL PRIMARY KEY,
                                "description" varchar
                                );
                                '''

    sql_alter_table_account_payable = '''ALTER TABLE "account_payable" ADD FOREIGN KEY ("type_id") REFERENCES "type" 
    ("id");'''

    sql_insert_new_type_accounts_payable = '''
        INSERT INTO "type" ("description") VALUES ('Contas a pagar')
    '''

    sql_insert_new_type_accounts_receivable = '''
        INSERT INTO "type" ("description") VALUES ('Contas a receber')
    '''

    cursor.execute(sql_insert_table_account_payable)
    cursor.execute(sql_insert_table_account_type)
    cursor.execute(sql_alter_table_account_payable)

    cursor.execute(sql_insert_new_type_accounts_payable)
    cursor.execute(sql_insert_new_type_accounts_receivable)

    conn.commit()
    conn.close()


def insert_new_account(type_id: int, unit_value: float, due_date: str, description: str):

    config = load_config()
    conn = connect(config)
    cursor = conn.cursor()

    sql_insert_account = '''
        INSERT INTO account_payable (unit_value, due_date, description, type_id) 
        VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql_insert_account, (unit_value, due_date + " 00:00:00", description, type_id))
    conn.commit()
    conn.close()


def insert_new_account_to_pay(unit_value: float, due_date: str, description: str):
    insert_new_account(1, unit_value, due_date, description)


def insert_new_account_to_receivable(unit_value: float, due_date: str, description: str):
    insert_new_account(2, unit_value, due_date, description)


def select_account_payable_by_type_id(type_id):
    try:

        config = load_config()
        conn = connect(config)
        cursor = conn.cursor()

        sql_select_account_payable = '''
            SELECT ap.*, t.description 
            FROM account_payable ap 
            INNER JOIN "type" t ON ap.type_id = t.id 
            WHERE ap.type_id = %s
        '''

        cursor.execute(sql_select_account_payable, (type_id,))

        rows = cursor.fetchall()

        for count, row in enumerate(rows):
            print("Conta número: " + str(count + 1))
            print("Valor: " + str(row[1]))
            print("Data da conta: " + str(row[2]))
            print("Descrição da conta: " + str(row[3]))
            print("Tipo da conta: " + str(row[5]))
            print("-------------------------------------")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Erro ao tentar pegar contas pelo tipo:", e)


def calculate_balance():
    try:

        config = load_config()
        conn = connect(config)
        cursor = conn.cursor()

        sql_sum_accounts_receivable = '''
            SELECT SUM(unit_value) FROM account_payable WHERE type_id = 2
        '''

        cursor.execute(sql_sum_accounts_receivable)
        sum_accounts_receivable = cursor.fetchone()[0] or 0

        sql_sum_accounts_payable = '''
            SELECT SUM(unit_value) FROM account_payable WHERE type_id = 1
        '''

        cursor.execute(sql_sum_accounts_payable)
        sum_accounts_payable = cursor.fetchone()[0] or 0

        balance = sum_accounts_receivable - sum_accounts_payable

        print("Salado atual da empresa:", balance)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error ao tentar calcular contas", e)