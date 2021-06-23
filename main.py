import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(1)  # ("Videos/test.mp4")
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

hand_detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = hand_detector.findHands(img)
    lmList = hand_detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]  # doigt 1 (pouce)
        x2, y2 = lmList[20][1], lmList[20][2]  # doigt 2 (index)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Dessine les cercles et la ligne entre les doigts (avec le cercle de moitié)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)  # obtient la longueur entre les doigts
        # print(length)

        # Intervalle main : 50 - 300
        # Intervalle volume : -65 - 0

        vol = np.interp(length, [50, 300], [minVol, maxVol])  # interpole l'intervalle 50 - 300 avec le volume min/max
        volBar = np.interp(length, [50, 300], [400, 150])  # convertir l'intervalle 50 - 300 en barre de volume
        volPer = np.interp(length, [50, 300], [0, 100])  # convertit l'intervalle 50 - 300 en pourcentage
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:  # change la couleur du cercle central si doigts collés
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)  # R, V, B (0, 255, 0)

    # Affichage des infos
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()  # (mili)seconde actuelle (epoch linux)
    fps = 1 / (cTime - pTime)  # fps = 1 / (seconde actuelle - seconde précédente)
    pTime = cTime  # met à jour la seconde précédente à chaque affichage d'image
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)  # montre la video

    if cv2.waitKey(1) == 27:
        break  # echap pour quitter

