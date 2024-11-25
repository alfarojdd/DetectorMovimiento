import cv2
import numpy as np
from email_utils import send_email
import time
import os

def detect_motion_with_alerts():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error al abrir la cámara")
        return

    print("Esperando a que la cámara se estabilice...")
    time.sleep(2)

    _, frame1 = cap.read()
    _, frame2 = cap.read()

    motion_detected = False
    recording = False

    max_recording_time = 1
    thresh_recording_time = 1
    recording_time = 0

    while cap.isOpened():
        
        #Detección del movimiento
        
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (15, 15), 0)
        _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=20)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) >= 500:  
                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Motion Detector", frame1)

        #Crear funcion para grabar a la vez que se hace el bucle para comprobar si hay movimiento

        if motion_detected and not recording:
            video_path = "motion_video.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))  # Graba con resolución de 640x480 y 20 fps
            start_time = time.time()
            recording_time = 0
            recording = True
            print(f'Iniciando grabación')
        elif motion_detected:
            recording_time = recording_time + time.time() - start_time
            start_time = time.time()

        if recording:
            if time.time() - start_time < thresh_recording_time and recording_time <= max_recording_time:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                cv2.imshow("Recording Video", frame)  # Ocultar despues
            else:
                out.release() 
                cv2.destroyWindow("Recording Video")
                send_email("Movimiento Detectado", "Se ha detectado movimiento en tu webcam", "TUCORREO", video_path)
                recording = False
                print('Fin de la grabación')
                if os.path.exists(video_path):
                    os.remove(video_path)
            
        motion_detected = False
        frame1 = frame2
        _, frame2 = cap.read()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_motion_with_alerts()
