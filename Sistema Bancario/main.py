from contas import Conta, ContaPoupanca
from banco import Banco


#Utilização da classe Conta
c1 = Conta(3,senha=1234,titular="João",saldoi=500)

b1 = Banco()
b1.atendimento()

#c1.deposito(300)
#c1.saque(1234, 200)


#Utilização da classe ContaPoupanca
#cp = ContaPoupanca(2,"Maria",1234,saldoi=1200)
#cp.exibeDados(1234)
#cp.simulaRendimento(12)