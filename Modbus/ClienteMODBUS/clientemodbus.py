from time import sleep
from pymodbus.client import ModbusTcpClient

class ClienteMODBUS():
    """
    Classe Cliente MODBUS
    """
    def __init__(self, server_ip,porta,scan_time=1):
        """
        Construtor
        """
        self._cliente = ModbusTcpClient(host=server_ip,port = porta)
        self._scan_time = scan_time

    def atendimento(self):
        """
        Método para atendimento do usuário
        """
        self._cliente.connect()

        try:
            atendimento = True
            while atendimento:
                sel = input("Deseja realizar uma leitura, escrita ou configuração? (1- Leitura | 2- Escrita | 3- Configuração |4- Sair): ")
                
                if sel == '1':
                    tipo = input ("""Qual tipo de dado deseja ler? (1- Holding Register |2- Coil |3- Input Register |4- Discrete Input |5- Holding Register: Ponto Flutuante) :""")
                    addr = input (f"Digite o endereço da tabela MODBUS: ")
                    if (input("Deseja ler um bit? (s/n): ") == 's'):
                            bit_pos = input("Digite a posição do bit (0-15): ")
                            nvezes = input("Digite o número de vezes que deseja ler: ")
                            for i in range(0,int(nvezes)):
                                print(f"Leitura {i+1}: {self.lerBit(int(addr), int(bit_pos))}")
                                sleep(self._scan_time)
                            continue
                        
                    nvezes = input ("Digite o número de vezes que deseja ler: ")
                    for i in range(0,int(nvezes)):
                        print(f"Leitura {i+1}: {self.lerDado(int(tipo), int(addr))}")
                        sleep(self._scan_time)
                elif sel =='2':
                    tipo = input ("""Qual tipo de dado deseja escrever? (1- Holding Register |2- Coil | 3- Holding Register: Ponto flutuante) :""")
                    addr = input (f"Digite o endereço da tabela MODBUS: ")
                    if (input("Deseja escrever um bit? (s/n): ") == 's'):
                            bit_pos = input("Digite a posição do bit (0-15): ")
                            valor = input("Digite o valor do bit (0 ou 1): ")
                            self.escreveBit(int(addr), int(bit_pos), int(valor))
                            continue
                    
                    valor = input (f"Digite o valor que deseja escrever: ")
                    self.escreveDado(int(tipo), int(addr), valor)

                elif sel=='3':
                    scant = input("Digite o tempo de varredura desejado [s]: ")
                    self._scan_time = float(scant)

                elif sel =='4':
                    self._cliente.close()
                    atendimento = False
                else:
                    print("Seleção inválida")
        except Exception as e:
            print('Erro no atendimento: ',e.args)

    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.read_holding_registers(addr,1)[0]
        
        if tipo == 2:
            return self._cliente.read_coils(addr,1)[0]

        if tipo == 3:
            return self._cliente.read_input_registers(addr,1)[0]

        if tipo == 4:
            return self._cliente.read_discrete_inputs(addr,1)[0]
        
        if tipo == 5:
            regs = self._cliente.read_holding_registers(address=addr, count=2 )
            print(f"Lendo ponto flutuante: {regs.registers}")
            print(f"Tipo de dado: ", type(regs.registers))
            print(f"Identificador da Mensagem: {regs.transaction_id}")
            return self._cliente.convert_from_registers(regs.registers, data_type = self._cliente.DATATYPE.FLOAT32, word_order='big')
        


    def escreveDado(self, tipo, addr, valor):
        """
        Método para a escrita de dados na Tabela MODBUS
        """
        if tipo == 1:
            return self._cliente.write_single_register(addr,valor)
        if tipo == 2:
            return self._cliente.write_single_coil(addr,valor)
        if tipo == 3:
            regs = self._cliente.convert_to_registers(float(valor),data_type = self._cliente.DATATYPE.FLOAT32, word_order='big')
            print(f"Escrevendo ponto flutuante: {regs}")
            return self._cliente.write_registers(addr, regs)

    def escreveBit(self, addr, bit_pos, valor):
        reg = self._cliente.read_holding_registers(address=addr,count=1)
        binario_str = bin(reg.registers[0])[2:].zfill(16)
        binario_list = [int(bit) for bit in binario_str]
        binario_list[bit_pos] = valor
        binario_list = list(reversed(binario_list))
        binario_str = ''.join(str(bit) for bit in binario_list)
        print(f"binario antes da escrita: {binario_str}")
        reg_value = int(binario_str, 2)
        return self._cliente.write_register(address=addr, value=reg_value)
    
    def lerBit(self, addr, bit_pos):
        reg = self._cliente.read_holding_registers(address=addr, count=1)
        binario_str = bin(reg.registers[0])[2:].zfill(16)
        binario_list = [int(bit) for bit in binario_str]
        binario_list = list(reversed(binario_list))
        return binario_list[bit_pos]
            
