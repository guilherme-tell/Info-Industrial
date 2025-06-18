from contas import Conta, ContaPoupanca

class Banco():
    __numContas = 4
    __tam = 0
    __pos = 0
    __contas = []
    contaCliente = 0

    def __init__(self):
           
           self.__senhaMestre = 9999
           self.contas = []

           self.__contas.append(Conta(1, 'Guilherme', 1234, 300))
           self.__contas.append(Conta(2, 'Maria', 1111, 200))           

    def verSenhaGerente(self, insenha):
        return insenha == self._senhaMestre
    
    def buscaContas(self, numero):
        for conta in self.__contas:
            if conta.numero == numero:
                return conta
        return None

    def atendimento(self):

        valor = 0
        while 1:
            atendimento = True
            numC = int(input("Digite o número da conta:"))

            contaCliente = self.buscaContas(numC)

            if contaCliente == None:
                print("Conta Inválida")
            else:
                insenha = int(input("Digite a senha da conta:"))

                if contaCliente.validaSenha(insenha) == 1:
                    print("Olá, ", contaCliente.titular)

                    while atendimento == 1:
                        op = int(input("Qual operação deseja fazer? (1 - Saque, 2 - Deposito, 3 - Ver Saldo, 4 - Transferência, 5 - Sair)."))

                        match op:
                            case 1:
                                valor = int(input("Digite o valor para saque:"))
                                contaCliente.saque(insenha, valor)
                            case 2:
                                valor = int(input("Digite o valor para depósito:"))
                                contaCliente.deposito(valor)
                            case 3:
                                print("Valor do Saldo:",contaCliente.getSaldo(insenha))
                            case 4:
                                valor = int(input("Digite o valor para transferência:"))
                                destino = int(input("Digite o número da conta de destino:"))
                                contaDestino = self.buscaContas(destino)
                                if contaDestino is None:
                                    print("Conta Destino Inválida!")
                                else:
                                    contaCliente.transferencia( valor, contaDestino)
                            case 5:
                                atendimento = False
                            
                            case _:
                                print("Operação Inválida!")
                                atendimento = False

                else:
                    print("Senha Inválida!")


