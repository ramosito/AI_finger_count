import cv2
import mediapipe as mp
import serial
import time

PORT_SERIE = "COM3"

camera = cv2.VideoCapture(0)
arduino = serial.Serial(PORT_SERIE, 9600, timeout=1)
time.sleep(2)

mp_hands = mp.solutions.hands
mp_dessin = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

BOUTS = [4, 8, 12, 16, 20]
dernier_envoi = -1

read, storage = camera.read()
while read:
    storage = cv2.flip(storage, 1)
    image_rgb = cv2.cvtColor(storage, cv2.COLOR_BGR2RGB)
    resultats = hands.process(image_rgb)

    nb_doigts = 0
    if resultats.multi_hand_landmarks:
        main = resultats.multi_hand_landmarks[0]
        cote = resultats.multi_handedness[0].classification[0].label
        mp_dessin.draw_landmarks(storage, main, mp_hands.HAND_CONNECTIONS)
        points = main.landmark

        if cote == "Right":
            if points[4].x < points[3].x:
                nb_doigts += 1
        else:
            if points[4].x > points[3].x:
                nb_doigts += 1

        for bout in BOUTS[1:]:
            if points[bout].y < points[bout - 2].y:
                nb_doigts += 1

    if nb_doigts != dernier_envoi:
        arduino.write(f"{nb_doigts}\n".encode())
        dernier_envoi = nb_doigts

    cv2.putText(storage, f"Doigts : {nb_doigts}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
    cv2.imshow("Camera", storage)

    if cv2.waitKey(1) == ord("q"):
        break
    read, storage = camera.read()

camera.release()
arduino.close()
cv2.destroyAllWindows()