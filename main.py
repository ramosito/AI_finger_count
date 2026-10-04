import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)

read, storage = camera.read()
while read:
    touche = cv2.waitKey(1)
    if touche == ord("q"):
        camera.release()
        cv2.destroyAllWindows()
        break
    else :
        read, storage = camera.read()
        cv2.imshow("Camera", storage)


RGB = cv2.cvtColor(storage, cv2.COLOR_BGR2RGB)

mp_hands = mp.solutions.Hands

hands = mp_hands.Hands()

resultats = hands.process(RGB)
