import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
import time

# GPIO SETUP 
GPIO.setmode(GPIO.BCM)
LED_PIN = 23
LED_PIN2 = 24
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Start with LED OFF

GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.output(LED_PIN2, GPIO.LOW)  # Start with LED OFF

#  Mediapipe Setup 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        gesture = "No Hand"

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                lm = hand.landmark

                fingers = []

                # Thumb (ignored later)
                fingers.append(1 if lm[4].x > lm[3].x else 0)

                # Other fingers
                fingers.append(1 if lm[8].y < lm[6].y else 0)    # Index
                fingers.append(1 if lm[12].y < lm[10].y else 0)  # Middle
                fingers.append(1 if lm[16].y < lm[14].y else 0)  # Ring
                fingers.append(1 if lm[20].y < lm[18].y else 0)  # Little

                finger_count = sum(fingers[1:])  # Count excluding thumb

                if finger_count == 0:
                    gesture = "FIST"
                elif finger_count == 1:
                    gesture = "ONE"
                elif finger_count == 2:
                    gesture = "PEACE"
                elif finger_count == 4:
                    gesture = "OPEN PALM"
                else:
                    gesture = "UNKNOWN"

                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                # LED CONTROL 
                if gesture == "ONE":
                    GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
                else:
                    GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED OFF
                    
                if gesture == "PEACE":
                    GPIO.output(LED_PIN2, GPIO.HIGH)  # Turn LED ON
                else:
                    GPIO.output(LED_PIN2, GPIO.LOW)   # Turn LED OFF

        else:
            # No hand detected ? turn LED OFF
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(LED_PIN2, GPIO.LOW)

        cv2.putText(frame, f'Gesture: {gesture}',
                    (30, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3)

        cv2.imshow("Gesture Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()  # Reset GPIO pins
