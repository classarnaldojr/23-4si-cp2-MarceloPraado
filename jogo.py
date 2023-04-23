import cv2

import numpy as np

import matplotlib.pyplot as plt

video = cv2.VideoCapture('pedra-papel-tesoura.mp4') #Captura do Vídeo

if not video.isOpened():
    raise Exception("Video deu pau") #Expection se o Vídeo não abrir


while True:

    #pontos_jogador_1 = 0
    #pontos_jogador_2 = 0

    ret, frame = video.read() #Ler o frame do vídeo

    foto = frame.copy() #Copio o frame para fazer outro retorno

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Filtro de Cinza

    img = cv2.blur(img_hsv, (15, 15), 0)  # Blur na Imagem para ficar mais clara a detecção

    lower_hsv_1 = np.array([0, 20, 10])  # Ranges para HSV
    higher_hsv_1 = np.array([18, 200, 200])  # Ranges para HSV

    lower_hsv_2 = np.array([0, 1, 1])  # Ranges para HSV
    higher_hsv_2 = np.array([255, 150, 250])  # Ranges para HSV

    mask_1 = cv2.inRange(img, lower_hsv_1, higher_hsv_1)  # Máscara 1

    mask_2 = cv2.inRange(img, lower_hsv_2, higher_hsv_2)  # Máscara 2

    img_filtro = cv2.bitwise_or(mask_1, mask_2)  # Imagem filtrada (para calcular Massa do Objeto)

    contours, _ = cv2.findContours(img_filtro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Encontrar os Contornos da Imagem img_filtro

    cv2.drawContours(foto, contours, -1, [0, 0, 0], 3) #Desenhando os Contornos de Preto onde encontrar

    c1 = contours[1] #Puxando Jogador 1
    c2 = contours[0] #Puxando Jogador 2

    sla = cv2.moments(c1) #Retirando Dicionário dos Contornos do Jogador 1
    sla2 = cv2.moments(c2) #Retirando Dicionário dos Contornos do Jogador 2

    area1 = int(sla['m00']) #Retirando Valor referente a área total do objeto (mão do jogador 1)
    area2 = int(sla2['m00'])#Retirando Valor referente a área total do objeto (mão do jogador 2)

    # Lógica para definir os tipos de objeto de acordo com sua área total (Jogador 1)
    if area1 < 58000:
        area1 = "Tesoura"

    elif area1 > 58000 and area1 < 70000:
        area1 = "Pedra"

    elif area1 > 70000:
        area1 = "Papel"

    # Lógica para definir os tipos de objeto de acordo com sua área total (Jogador 2)
    if area2 < 58000:
        area2 = "Tesoura"

    elif area2 > 58000 and area2 < 70000:
        area2 = "Pedra"

    elif area2 > 70000:
        area2 = "Papel"

    #Inversão para uma Das Detecções que foram processadas invertidas
    if area1 == "Pedra" and area2 == "Tesoura":
        area1 = "Tesoura"
        area2 = "Pedra"

    # SISTEMA DE PONTUAÇÕES
    if area1 == area2:
        resultado = "Empate!"

    elif (area1 == "Tesoura" and area2 == "Papel"):
        resultado = "Jogador 1 Venceu!"
        #pontos_jogador_1 = pontos_jogador_1 + 1
    elif (area1 == "Papel" and area2 == "Tesoura"):
        resultado = "Jogador 2 Venceu!"
        #pontos_jogador_2 = (pontos_jogador_2 + 1)
    elif (area1 == "Pedra" and area2 == "Tesoura"):
        resultado = "Jogador 1 Venceu!"
        #pontos_jogador_1 = (pontos_jogador_1 + 1)
    elif (area1 == "Tesoura" and area2 == "Pedra"):
        resultado = "Jogador 2 Venceu!"
        #pontos_jogador_2 = (pontos_jogador_2 + 1)
    elif (area1 == "Papel" and area2 == "Pedra"):
        resultado = "Jogador 1 Venceu!"
        #pontos_jogador_1 = (pontos_jogador_1 + 1)
    elif (area1 == "Pedra" and area2 == "Papel"):
        resultado = "Jogador 2 Venceu!"
        #pontos_jogador_2 = (pontos_jogador_2 + 1)

    #Inserindo as Informações no Frame

    #Título
    (cv2.putText(foto,
                 "Pedra, Papel e Tesoura: The Game",
                 (415, 50),
                 cv2.FONT_HERSHEY_SIMPLEX,          #TÍTULO
                 2, (0, 0, 255), 2,
                cv2.LINE_AA))

    #Jogada do Jogador 1
    (cv2.putText(foto,
                 ("Jogador 1: " + str(area1)),
                 (25, 150),                         #Qual a Jogada do Jogador 1
                 cv2.FONT_HERSHEY_SIMPLEX,
                 2, (0, 0, 0), 2, cv2.LINE_AA))
    #Jogada do Jogador 2
    (cv2.putText(foto,
                 ("Jogador 2: " + str(area2)),
                 (25, 250),
                 cv2.FONT_HERSHEY_SIMPLEX,          #Qual a Jogada do Jogador 2
                 2, (0, 0, 0), 2, cv2.LINE_AA))
    #Resultado da Jogada
    (cv2.putText(foto,
                 str(resultado),
                 (650, 1000),
                 cv2.FONT_HERSHEY_SIMPLEX,          #Vencedor da Rodada
                 2,
                 (0, 0, 255), 2, cv2.LINE_AA))
    #Pontuação do Jogador 1
    #(cv2.putText(foto,
    #             ("Pontos Player 1 = " + str(pontos_jogador_1)),
    #             (1100, 150),                            #Pontuação Jogador 1
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             2,(0, 0, 255), 2, cv2.LINE_AA))

    # Pontuação do Jogador 2
    #(cv2.putText(foto,
    #             ("Pontos Player 2 = " + str(pontos_jogador_2)),
    #             (1100, 250),
    #             cv2.FONT_HERSHEY_SIMPLEX,              #Pontuação Jogador 2
    #             2,(0, 0, 255), 2, cv2.LINE_AA))

    #Reduzindo tamanho da Renderização para os dois vídeos caberem na tela
    frame = cv2.resize(img_filtro, (640, 480))

    img_final = cv2.resize(foto, (640, 480))

    cv2.imshow("Maos Detectadas", frame)

    cv2.imshow("Video Tratado", img_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if not ret:
        break

video.release()

cv2.destroyAllWindows()