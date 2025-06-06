import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand):
    tips = [8, 12, 16, 20]
    count = 0
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            count += 1
    return count

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(handLms)

            if fingers >= 4:
                pyautogui.keyDown('right')
                pyautogui.keyUp('left')
                cv2.putText(img, 'Accelerating...', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            elif fingers == 0:
                pyautogui.keyDown('left')
                pyautogui.keyUp('right')
                cv2.putText(img, 'Braking...', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            else:
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
                cv2.putText(img, 'Neutral', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    else:
        pyautogui.keyUp('left')
        pyautogui.keyUp('right')

    cv2.imshow("Hand Gesture Control", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
