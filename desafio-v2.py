import textwrap

def menu():
    menu = """\n
    =============== MENU ===============

    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova Conta
    [5]\tListar Contas
    [6]\tNovo Usuário
    [7]\tSair

    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")

    else:
        print("\n@@@ A operação não pode ser concluída! Informe um valor válido. @@@")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, quantidade_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = quantidade_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ A operação não pode ser concluída! Saldo insuficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ A operação não pode ser concluída! O valor informado excede o limite disponível. @@@")

    elif excedeu_saques:
        print("\n@@@ A operação não pode ser concluída! Número máximo de saques diários excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        quantidade_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ A operação não pode ser concluída! Informe um valor válido. @@@")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n=============== EXTRATO ===============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("=======================================")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe um usuário cadastrado com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD-MM-AAAA): ")
    endereco = input("Informe o endereço (Logradouro, Número - Bairro - Cidade/Sigla Estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n=== Usuário cadastrado com sucesso! ===")

def filtar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    quantidade_saques = 0
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                quantidade_saques=quantidade_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_usuario(usuarios)

        elif opcao == "7":
            print("\n=== Obrigado(a) por utilizar nossos serviços. Volte Sempre! ===")
            break

        else:
            print("\n@@@ A operação não pode ser concluída! Selecione uma opção válida para prosseguir. @@@")

main()
