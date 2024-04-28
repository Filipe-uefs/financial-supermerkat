from usecases.account_payable_dao import (create_tables, insert_new_account_to_pay, insert_new_account_to_receivable,
                                          select_account_payable_by_type_id, calculate_balance)


def menu():

    create_tables()

    while True:

        action = input("Insira a ação que deseja realizar\n(1) Registrar uma nova conta\n(2) Registrar conta a "
                       "receber\n(3) Visualizar contas a pagar\n(4) Visualizar contas a receber\n(5) Calcular "
                       "saldo atual\n(6) Sair\n")

        if action == '1':
            unit_value = float(input("Entre o valor: "))
            due_date = input("Entre a data de vencimento (YYYY-MM-DD): ")
            description = input("Entre a da descrição da conta: ")
            insert_new_account_to_pay(unit_value, due_date, description)

        elif action == '2':

            unit_value = float(input("Entre o valor: "))
            due_date = input("Entre a data de vencimento (YYYY-MM-DD): ")
            description = input("Entre a da descrição da conta: ")
            insert_new_account_to_receivable(unit_value, due_date, description)

        elif action == '3':
            select_account_payable_by_type_id(1)

        elif action == '4':
            select_account_payable_by_type_id(2)

        elif action == '5':
            calculate_balance()

        elif action == '6':
            break

        else:
            pass
