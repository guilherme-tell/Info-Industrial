from servidor import Servidor

serv = Servidor("localhost",9000) #127.0.0.1 qualquer interface de rede do computador vai receber o serviço
serv.start()

