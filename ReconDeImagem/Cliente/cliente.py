import socket
import cv2
import numpy as np

class Cliente():
    """
    Classe Cliente - API Socket
    """
    def __init__(self, server_ip, port):
        """
        Construtor da classe Cliente
        """
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def start(self):
        """
        Método que inicializa a execução do Cliente
        """
        endpoint = (self.__server_ip,self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão realizada com sucesso!")
            self.__method()
        except:
            print("Servidor não disponível")

    
    def __method(self):
        """
        Método que implementa as requisições do cliente
        """
        try:
            # msg = ''
            # while True:
            #     msg = input("Digite a operação (x para sair): ")
            #     if msg == '':
            #         continue
            #     elif msg == 'x':
            #         break
            #     self.__tcp.send(bytes(msg,'ascii'))
            #     resp = self.__tcp.recv(1024)
            #     print("= ",resp.decode('ascii'))
            # self.__tcp.close()
            while True:
                image_path = 'faces/image_0001.jpg'
                image = cv2.imread(image_path)
                _, img_bytes = cv2.imencode('.jpg', image)

                img_bytes = bytes(img_bytes)
                tamanho_da_imagem_codificado = len(img_bytes).to_bytes(4, 'big')

                # Envia o tamanho da imagem codificado
                self.__tcp.send(tamanho_da_imagem_codificado)
                self.__tcp.send(img_bytes)
                print("Imagem enviada com sucesso!")

                # Recebe a resposta do servidor
                tamanho_da_imagem_processada = self.__tcp.recv(1024)
                tamanho_da_imagem_processada = int.from_bytes(tamanho_da_imagem_processada, 'big')

                imagem_recebida_bytes = b''
                for i in range(round(tamanho_da_imagem_processada / 1024)):
                    imagem_recebida_bytes += self.__tcp.recv(1024)
                    
                img = cv2.imdecode(np.frombuffer(imagem_recebida_bytes, np.uint8), cv2.IMREAD_COLOR)

                cv2.imshow('Imagem Processada', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)
