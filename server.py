'''
    Simple udp Socket server
    Silver Moon (m00n.silv3r@gmail.com)
'''
 
import socket
import sys
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

listaJogadores = []
 
# Datagram (udp) Socket
try :
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print '--> Socket criado'
except socket.error, mensagem:
    print '--> Falha ao criar Socket. Codigo de erro: ' + str(mensagem[0]) + '; Mensagem: ' + mensagem[1]
    sys.exit()
 
 
# Bind Socket to local host and port
try:
    Socket.bind((HOST, PORT))
except socket.error , mensagem:
    print 'Erro no estabelecimento de ligacao. Codigo de erro: ' + str(mensagem[0]) + '; Mensagem: ' + mensagem[1]
    sys.exit()
     
print 'Estabelecimento de ligacao efectuado com sucesso'
 
#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    data = Socket.recvfrom(1024)
    dataReceived = data[0]
    addressClient = data[1]

    mensagem = ''
    dataReceived = dataReceived.split(' ', 1)

    if not dataReceived: 
        break

    elif dataReceived[0] == 'Registo:':                                                 #Caso o jogador se tente registar
        variavel = 0
        for jogador in listaJogadores:
            if jogador[0] == dataReceived[1]:
                variavel = 1
                break
        if variavel == 1: 
            Socket.sendto('Nome utilizado', addressClient)                              #Nome utilizado            
        else:   
            listaJogadores.append([dataReceived[1], addressClient, 'Livre'])            #Acrescenta jogador a lista
            Socket.sendto('Ok', addressClient)

    
    elif dataReceived[0] == 'Lista':                                                    #Caso o jogador tente aceder a lista
        for jogador in listaJogadores:                                                  #E apresentada a lista com todos os jogadores registados
            mensagem +=  '\n' + jogador[0] + ' --> ' + jogador[2]
        Socket.sendto(mensagem , addressClient)
    
    elif dataReceived[0] == 'Convite:':                                                 #Caso o jogador tente fazer um convite
        variavel = 0
        for jogador in listaJogadores:
            if addressClient == jogador[1]:                                             #Nao permitir que o jogador se convide a si proprio
                if jogador[0] == dataReceived[1]:
                    Socket.sendto('O jogo e multiplayer' , addressClient)                
                    variavel = 1
            else:
                if jogador[0] == dataReceived[1]:
                        if jogador[2] == 'Livre':                                       #Passa o estado do jogador que convidou a ocupado
                            variavel = 1
                            jogadorR = jogador[1]
                            for jogador in listaJogadores:
                                if jogador[1] == addressClient:
                                    Socket.sendto('Ok' , addressClient)
                                    Socket.sendto('Convite: ' + jogador[0], jogadorR)
                                    jogador[2] = 'Ocupado'
                        else:
                            variavel = 1                                                #Jogador ocupado
                            Socket.sendto('Jogador Ocupado',addressClient)
        if variavel == 0:                                                               #Jogador inexistente
            Socket.sendto('Jogador Inexistente', addressClient)

    elif dataReceived[0] == 'ConviteR:':                                                #Resposta do jogador2 ao convite
        Socket.sendto('Ok' , addressClient)
        dataReceived1 = dataReceived[1].split(' ', 1)
        for jogador in listaJogadores:
            if jogador[0] == dataReceived1[1]:
            	var = jogador[1]
                if dataReceived1[0] == 'Aceite':                                        #Caso tenha aceite
                    for jogador in listaJogadores:
                        if jogador[1] == addressClient:                                 #atualiza o estado do jogador2 para ocupado
                            jogador[2] = 'Ocupado'
                            Socket.sendto('ConviteR: Aceite ' + jogador[0], var)

                else:                                                                   #Caso tenha recusado
                    Socket.sendto('ConviteR: Recusado', jogador[1])
                    jogador[2] = 'Livre'                                                #atualiza o estado do jogador2 para livre

    elif dataReceived[0] == 'Jogada:':                                                  #Enviar a jogada de um jogador para outro
        Socket.sendto('Ok', addressClient)
        dataReceived1 = dataReceived[1].split(' ', 1)
        for jogador in listaJogadores:
            if jogador[1] == addressClient:
                jogadorR = jogador[0]
                for jogador1 in listaJogadores:
                    if dataReceived1[1] == jogador1[0]:
                        Socket.sendto('Jogada: ' + dataReceived1[0] + ' ' + jogadorR, jogador1[1])

    elif dataReceived[0] == 'Fim:':                                                  #Enviar o fim de jogo de um jogador para outro   
        dataReceived1 = dataReceived[1].split(' ', 1)
        if dataReceived1[0]== 'Ganhei':
            for jogador in listaJogadores:
                if jogador[0] == dataReceived1[1]:
                    Socket.sendto('Fim: Perdeste', jogador[1])
                    jogador[2] = 'Livre'
                    for jogador in listaJogadores:
                        if jogador[1] == addressClient:
                            jogador[2] = 'Livre'
        if dataReceived1[0]== 'Empatamos':                                          #Empate
            for jogador in listaJogadores:
                if jogador[0] == dataReceived1[1]:
                    Socket.sendto('Fim: Empatamos', jogador[1])
                    jogador[2] = 'Livre'
                    for jogador in listaJogadores:
                        if jogador[1] == addressClient:
                            jogador[2] = 'Livre'

    else:
    	continue
        Socket.sendto('OK...' + dataReceived , addressClient)
        print 'Message[' + addressClient[0] + ':' + str(addressClient[1]) + '] - ' + dataReceived.strip()
  
socket.close()