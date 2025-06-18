import socket
import cv2
import numpy as np
import os

class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                con, client = self.__tcp.accept()
                self._service(con, client)
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        """
        Método que implementa o serviço de reconhecimento de imagem
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        # while True:
        #     try:
        #         msg = con.recv(1024)
        #         msg_s = str(msg.decode('ascii'))
        #         resp = eval(msg_s)
        #         con.send(bytes(str(resp), 'ascii'))
        #         print(client, " -> requisição atendida")
        #     except OSError as e:
        #         print("Erro de conexão ", client, ": ", e.args)
        #         return
        #     except Exception as e:
        #         print("Erro nos dados recebidos pelo cliente ",
        #               client, ": ", e.args)
        #         con.send(bytes("Erro", 'ascii'))
        #         return


        while True:

            try:
                imag_tam = con.recv(1024)
                for i in range(imag_tam/1024):
                    imag_bytes = con.recv(1024)

                img_tam = int.from_bytes(imag_tam, 'big')
                img = cv2.imdecode(np.frombuffer(imag_bytes, np.uint8), cv2.IMREAD_COLOR)

                xml_classificador = os.path.join(os.path.relpath(
                    cv2.__file__).replace('__init__.py', ''), 'data\haarcascade_frontalface_default.xml')
                face_cascade = cv2.CascadeClassifier(
                    xml_classificador)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                con.send(bytes(img))
                print(client, "-> Imagem Processada")

            except OSError as e:
                print("Erro de conexão", client, ":", e.args)
                con.send(bytes("Erro", 'ascii'))
                return
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente", client, ":", e.args)
                con.send(bytes("Erro", 'ascii'))
                return
