'''
    udp socket client
    Silver Moon
'''
 
import socket   #for sockets
import sys  #for exit
 
# create dgram udp socket
try:
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;
dataReceived = '';
tabuleiro = ['1','2','3','4','5','6','7','8','9']

#Fazer o registo do jogador
while dataReceived != 'Ok':
    try:
        nome = raw_input('Introduza um nome para se registar: ')
        Socket.sendto('Registo: ' + nome, (host, port))
        Socket.settimeout(5)
        data = Socket.recvfrom(1024)
        dataReceived = data[0]
        if dataReceived != 'Ok':
            print 'Erro: ' + dataReceived
        else:
            print 'Registo feito com sucesso'
    except socket.timeout:
        print 'servidor nao encontrado'
 
while(1) :
    
    mensagem = raw_input('Introduza a mensagem para enviar: ')
     
    try :
        #Set the whole string
        Socket.sendto(mensagem, (host, port))
         
        # receive data from server (data, addr)
        data = Socket.recvfrom(1024)
        dataReceived = data[0]
        addressSender = data[1]
        acabou = 0
        
        print 'A resposta do servidor e: ' + dataReceived
        dataReceived = dataReceived.split(' ', 1)

        if dataReceived[0] == 'Convite:':                                                             #Receber um convite
            mensagem = raw_input('Quer aceitar ou recusar? Aceite/Recusado: ')
            Socket.sendto('ConviteR: ' + mensagem + ' ' + dataReceived[1], (host, port))              #Se receber convites em simultaneo
            if mensagem == 'Aceite':
                data = Socket.recvfrom(1024)
                dataReceived = data[0]
                addressSender = data[1]
                dataReceived = dataReceived.split(' ', 1)
                while dataReceived[0] == 'Convite:':                                                   #Se aceitar o primeiro envia recusado para os outros
                    Socket.sendto('ConviteR: Recusado' + ' ' + dataReceived[1], (host, port))
                    data = Socket.recvfrom(1024)
                    dataReceived = data[0]
                    addressSender = data[1]
                    dataReceived = dataReceived.split(' ', 1)
                tabuleiro = ['1','2','3','4','5','6','7','8','9']
                print 'A resposta do servidor e: ' + data[0]
                while acabou == 0:                                                                      
                    data = Socket.recvfrom(1024)
                    dataReceived = data[0]
                    addressSender = data[1]
                    dataReceived = dataReceived.split(' ', 1)
                    if dataReceived[0] == 'Jogada:':
                        dataReceived1 = dataReceived[1].split(' ', 1)
                        tabuleiro[int(dataReceived1[0])-1] = 'X'
                    elif dataReceived[0] == 'Fim:':
                        var = dataReceived[1]
                        data = Socket.recvfrom(1024)
                        dataReceived = data[0]
                        addressSender = data[1]
                        dataReceived = dataReceived.split(' ', 1)
                        dataReceived1 = dataReceived[1].split(' ', 1)
                        tabuleiro[int(dataReceived1[0])-1] = 'X'
                        print '\n ' + tabuleiro[0]+' | '+tabuleiro[1]+' | '+tabuleiro[2]+'\n---+---+---\n '+tabuleiro[3]+' | '+tabuleiro[4]+' | '+tabuleiro[5]+'\n---+---+---\n '+tabuleiro[6]+' | '+tabuleiro[7]+' | '+tabuleiro[8]
                        print var
                        acabou = 1
                        break
                    print '\n ' + tabuleiro[0]+' | '+tabuleiro[1]+' | '+tabuleiro[2]+'\n---+---+---\n '+tabuleiro[3]+' | '+tabuleiro[4]+' | '+tabuleiro[5]+'\n---+---+---\n '+tabuleiro[6]+' | '+tabuleiro[7]+' | '+tabuleiro[8]
                    mensagem = raw_input('Introduza jogada: ')
                    while tabuleiro[int(mensagem)-1] != mensagem:
                        print 'Jogada invalida'
                        mensagem = raw_input('Introduza jogada: ')
                    tabuleiro[int(mensagem)-1] = 'O'
                    print '\n ' + tabuleiro[0]+' | '+tabuleiro[1]+' | '+tabuleiro[2]+'\n---+---+---\n '+tabuleiro[3]+' | '+tabuleiro[4]+' | '+tabuleiro[5]+'\n---+---+---\n '+tabuleiro[6]+' | '+tabuleiro[7]+' | '+tabuleiro[8]
                    if((tabuleiro[0] == 'O' and tabuleiro[1] == 'O' and tabuleiro[2] == 'O') or (tabuleiro[3] == 'O' and tabuleiro[4] == 'O' and tabuleiro[5] == 'O') or (tabuleiro[6] == 'O' and tabuleiro[7] == 'O' and tabuleiro[8] == 'O') or  
                        (tabuleiro[0] == 'O' and tabuleiro[3] == 'O' and tabuleiro[6] == 'O') or (tabuleiro[1] == 'O' and tabuleiro[4] == 'O' and tabuleiro[7] == 'O') or (tabuleiro[2] == 'O' and tabuleiro[5] == 'O' and tabuleiro[8] == 'O') or 
                        (tabuleiro[0] == 'O' and tabuleiro[4] == 'O' and tabuleiro[8] == 'O') or (tabuleiro[2] == 'O' and tabuleiro[4] == 'O' and tabuleiro[6] == 'O')):
                        acabou = 1
                        print 'Ganhei'
                        Socket.sendto('Fim: Ganhei ' + dataReceived1[1], (host, port))
                    Socket.sendto('Jogada: ' + mensagem + ' ' + dataReceived1[1], (host, port))
                    print 'A resposta do servidor e: ' + Socket.recvfrom(1024)[0]

        elif dataReceived[0] == 'ConviteR:':
            dataReceived1 = dataReceived[1].split(' ', 1)
            if dataReceived1[0] == 'Aceite':
                nrJogada = 1
                tabuleiro = ['1','2','3','4','5','6','7','8','9']
                while acabou == 0:
                    print '\n ' + tabuleiro[0]+' | '+tabuleiro[1]+' | '+tabuleiro[2]+'\n---+---+---\n '+tabuleiro[3]+' | '+tabuleiro[4]+' | '+tabuleiro[5]+'\n---+---+---\n '+tabuleiro[6]+' | '+tabuleiro[7]+' | '+tabuleiro[8]
                    mensagem = raw_input('Introduza jogada: ')
                    while tabuleiro[int(mensagem)-1] != mensagem:
                        print 'Jogada invalida'
                        mensagem = raw_input('Introduza jogada: ')
                    tabuleiro[int(mensagem)-1] = 'X'
                    nrJogada = nrJogada + 1
                    print '\n ' + tabuleiro[0]+' | '+tabuleiro[1]+' | '+tabuleiro[2]+'\n---+---+---\n '+tabuleiro[3]+' | '+tabuleiro[4]+' | '+tabuleiro[5]+'\n---+---+---\n '+tabuleiro[6]+' | '+tabuleiro[7]+' | '+tabuleiro[8]
                    if((tabuleiro[0] == 'X' and tabuleiro[1] == 'X' and tabuleiro[2] == 'X') or (tabuleiro[3] == 'X' and tabuleiro[4] == 'X' and tabuleiro[5] == 'X') or (tabuleiro[6] == 'X' and tabuleiro[7] == 'X' and tabuleiro[8] == 'X') or  
                        (tabuleiro[0] == 'X' and tabuleiro[3] == 'X' and tabuleiro[6] == 'X') or (tabuleiro[1] == 'X' and tabuleiro[4] == 'X' and tabuleiro[7] == 'X') or (tabuleiro[2] == 'X' and tabuleiro[5] == 'X' and tabuleiro[8] == 'X') or 
                        (tabuleiro[0] == 'X' and tabuleiro[4] == 'X' and tabuleiro[8] == 'X') or (tabuleiro[2] == 'X' and tabuleiro[4] == 'X' and tabuleiro[6] == 'X')):
                        acabou = 1
                        print 'Ganhei'
                        Socket.sendto('Fim: Ganhei ' + dataReceived1[1], (host, port))
                    elif (nrJogada == 6):
                        print 'Empatamos'
                        acabou = 1
                        Socket.sendto('Fim: Empatamos ' + dataReceived1[1], (host, port))
                    Socket.sendto('Jogada: ' + mensagem + ' ' + dataReceived1[1], (host, port))
                    print 'A resposta do servidor e: ' + Socket.recvfrom(1024)[0]
                    if(acabou != 1):
                        data = Socket.recvfrom(1024)
                        dataReceived = data[0]
                        addressSender = data[1]
                        dataReceived = dataReceived.split(' ', 1)
                        if dataReceived[0] == 'Jogada:':
                            dataReceived1 = dataReceived[1].split(' ', 1)
                            tabuleiro[int(dataReceived1[0])-1] = 'O'

                        elif dataReceived[0] == 'Fim:':
                            var = dataReceived[1]
                            data = Socket.recvfrom(1024)
                            dataReceived = data[0]
                            addressSender = data[1]
                            dataReceived = dataReceived.split(' ', 1)
                            dataReceived1 = dataReceived[1].split(' ', 1)
                            tabuleiro[int(dataReceived1[0])-1] = 'O'
                            print '\n ' + tabuleiro[0]+' | '+tabuleiro[1]+' | '+tabuleiro[2]+'\n---+---+---\n '+tabuleiro[3]+' | '+tabuleiro[4]+' | '+tabuleiro[5]+'\n---+---+---\n '+tabuleiro[6]+' | '+tabuleiro[7]+' | '+tabuleiro[8]
                            print var
                            acabou = 1


    except socket.error, mensagem:
        print 'Codigo de erro: ' + str(mensagem[0]) + '; Mensagem: ' + mensagem[1]
        sys.exit()