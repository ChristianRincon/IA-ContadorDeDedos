import cv2
import mediapipe as mp
import pyautogui

video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1) # Se puede modificar el valor a 2 para operar con ambas manos
mpDwaw = mp.solutions.drawing_utils

def resize_window():
    #Dimensiones de la pantalla actual
    screen_width, screen_height = pyautogui.size()

    # Cambia el tamaño de la ventana a las dimensiones de la pantalla
    cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagen', screen_width, screen_height)

resize_window()

while True:
    success, img = video.read()
    if not success:
        print("Error: No se pudo leer la imagen de la cámara.")
        break

    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    handPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    puntos = []

    if handPoints:
        for points in handPoints:
            #Descomentar para ver los landmarks
            #mpDwaw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)
            
            # Enumeramos los puntos
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                #Descomentar para ver los valores de los landmarks
                #cv2.putText(img, str(id), (cx, cy +10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                puntos.append((cx, cy))

            dedos = [8, 12, 16, 20]
            contador = 0

            if puntos:
                if puntos[4][0] < puntos[3][0]:
                    contador += 1
                for x in dedos:
                    if puntos[x][1] < puntos[x - 2][1]:
                        contador += 1

            #cv2.rectangle(img, (80, 10), (500, 110), (255, 0, 0), -1)
            cv2.putText(img, 'Usuario muestra ' + str(contador) + ' dedos', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    cv2.imshow('Imagen', img)
    
    # Cambiamos el tamaño de la ventana cuando se maximiza
    if cv2.getWindowProperty('Imagen', cv2.WND_PROP_FULLSCREEN) == cv2.WINDOW_FULLSCREEN:
        resize_window()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
