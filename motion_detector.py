import cv2
import numpy as np
from email_utils import send_email
import time

def detect_motion_with_alerts():
    time.sleep(10)
    cap = cv2.VideoCapture(0)  # Abre la cámara

    if not cap.isOpened():
        print("Error al abrir la cámara")
        return

    # Espera un poco para estabilizar la cámara antes de comenzar a capturar
    print("Esperando a que la cámara se estabilice...")
    time.sleep(2)  # Espera 2 segundos

    # Captura los primeros dos cuadros para la comparación
    _, frame1 = cap.read()
    _, frame2 = cap.read()

    alert_sent = False  # Para evitar múltiples alertas

    while cap.isOpened():
        # Calcula la diferencia entre los dos cuadros
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Aplica un umbral para detectar áreas de movimiento
        _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Encuentra los contornos de las áreas con movimiento
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Ignorar áreas pequeñas que no son movimiento significativo
                continue
            motion_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Si se detecta movimiento y no se ha enviado una alerta
        if motion_detected and not alert_sent:
            send_email("Movimiento Detectado", "Se ha detectado movimiento en tu webcam", "TUCORREO")
            alert_sent = True  # Evitar enviar múltiples alertas

        # Muestra el cuadro en la ventana
        cv2.imshow("Motion Detector", frame1)

        # Actualiza los cuadros
        frame1 = frame2
        _, frame2 = cap.read()

        # Verifica si la tecla 'q' es presionada para salir
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_motion_with_alerts()
