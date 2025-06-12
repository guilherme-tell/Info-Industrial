import socket

class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host           #atributo protegido da classe servidor
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #instanciando um objeto da classe socket
                                                                        #AF_INET -> address family qualquer dispositivo agrupado nesta familia
                                                                        #pode receber os beneficios deste serviço
                                                                        #SOCK_STREAM -> qual o protocolo da camada de transporte 
                                                                        #este em especifico é para o TCP,



    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        endpoint = (self._host, self._port)     # uma tupla, é um objeto imutavel, nao funciona passagem por atributo
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                con, client = self.__tcp.accept()       #con é o socket do cliente, é o objeto pra onde vou enviar dados para o cliente
                self._service(con, client)
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        """
        Método que implementa o serviço de calculadora
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        while True:
            try:
                msg = con.recv(1024)
                msg_s = str(msg.decode('ascii'))
                resp = eval(msg_s)
                con.send(bytes(str(resp), 'ascii'))
                print(client, " -> requisição atendida")
            except OSError as e:
                print("Erro de conexão ", client, ": ", e.args)
                return
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                      client, ": ", e.args)
                con.send(bytes("Erro", 'ascii'))
                return
