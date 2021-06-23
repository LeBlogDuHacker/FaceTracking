import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(1)  # ("Videos/test.mp4")
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=2, circle_radius=2)

frameWidth = 1920
frameHeight = 1080
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)  # construit le maillage
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:  # pour chaque maillage (de chaque visage trouvé)
            # Dessine le maillage sur le visage
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec)

    cTime = time.time()  # (mili)seconde actuelle (epoch linux)
    fps = 1 / (cTime - pTime)  # fps = 1 / (seconde actuelle - seconde précédente)
    pTime = cTime  # met à jour la seconde précédente à chaque affichage d'image
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)  # affiche les FPS
    cv2.imshow("Image", img)  # montre la video
    if cv2.waitKey(1) == 27:
        break  # echap pour quitter
cap.release()
