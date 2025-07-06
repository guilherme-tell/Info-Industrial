import socket
import cv2
import numpy as np
import os
import threading

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

        while True:

            try:
                imag_tam = con.recv(1024)
                img_tam = int.from_bytes(imag_tam, 'big')

                imag_bytes = bytes()

                for i in range(round(img_tam/1024)):
                    imag_bytes += con.recv(1024)
                img = cv2.imdecode(np.frombuffer(imag_bytes, np.uint8), cv2.IMREAD_COLOR)

                imagem_processada = self.rabisca(img)
                _, imagem_processada = cv2.imencode('.jpg', imagem_processada)
                imagem_processada_codificada = imagem_processada.tobytes()
                con.send(len(imagem_processada_codificada).to_bytes(4, 'big'))
                con.sendall(imagem_processada_codificada)
                print(client, "-> Imagem Processada")

            except OSError as e:
                print("Erro de conexão", client, ":", e.args)
                con.send(bytes("Erro", 'ascii'))
                return
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente", client, ":", e.args)
                return

    def rabisca(self, imagem):
        xml_classificador = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(xml_classificador)

        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(f"-> Faces detectadas: {len(faces)}")

        for (x, y, w, h) in faces:
            print(f"-> Desenhando retângulo em: (x={x}, y={y}, w={w}, h={h})")
            cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return imagem

class ServidorMT(Servidor):
    """
    Classe ServidorMT - API Socket Multithread
    """

    def __init__(self, host, port, nthreads=3):
        super().__init__(host, port)
        self._nthreads = nthreads
        self.__threadPool = {}
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):

        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)

            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                # 1. Aguarda uma nova conexão. Esta linha é bloqueante.
                con, client = self.__tcp.accept()
                print(f"Nova conexão recebida de {client}")

                # 2. Cria uma thread para cuidar deste cliente
                #    - target: a função que a thread vai executar (_service)
                #    - args: os argumentos para a função (a conexão e o cliente)
                #    - daemon=True: faz com que a thread seja encerrada se o programa principal fechar
                thread_cliente = threading.Thread(target=self._service, args=(con, client), daemon=True)
                
                # 3. Inicia a execução da thread.
                thread_cliente.start()
        
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args) 
