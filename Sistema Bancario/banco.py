from contas import Conta, ContaPoupanca

class Banco():
    __senhaMestre = 9999
    __numContas = 4
    __tam = 0
    __pos = 0
    __contas = []

    def __Init__(self):
           self.__contas.append(Conta(1234, 1, 'Guilherme', 'Corrente', 300))

    def verSenhaGerente(self, insenha):
        if insenha == self._senhaMestre:
            flag = 1