print("--- SISTEMA FIRA AUTONOMO INICIADO ---")

import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import sys

# ==============================
# CONFIG GPIO
# ==============================

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Motor esquerdo
IN1 = 17
IN2 = 27
ENA = 18

# Motor direito
IN3 = 22
IN4 = 23
ENB = 19

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwm_esq = GPIO.PWM(ENA, 1000)
pwm_dir = GPIO.PWM(ENB, 1000)

pwm_esq.start(0)
pwm_dir.start(0)

# ==============================
# FUNCOES MOVIMENTO
# ==============================

def frente():
    GPIO.output(IN1,1)
    GPIO.output(IN2,0)
    GPIO.output(IN3,1)
    GPIO.output(IN4,0)

def parar():
    pwm_esq.ChangeDutyCycle(0)
    pwm_dir.ChangeDutyCycle(0)

# ==============================
# CAMERA
# ==============================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar camera")
    GPIO.cleanup()
    sys.exit()

print("Camera conectada")
print("Sistema rodando")

# ==============================
# PARAMETROS
# ==============================

kp = 0.35
vel_base = 55

# ==============================
# LOOP PRINCIPAL
# ==============================

try:

    frente()

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.resize(frame,(320,240))
        altura, largura, _ = img.shape

        # cinza
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold
        _, mascara = cv2.threshold(cinza,80,255,cv2.THRESH_BINARY_INV)

        # filtro
        kernel = np.ones((5,5),np.uint8)
        mascara = cv2.morphologyEx(mascara,cv2.MORPH_CLOSE,kernel)

        # metade inferior
        area = mascara[altura//2:altura,:]

        M = cv2.moments(area)

        if M["m00"] > 0:

            cx = int(M["m10"]/M["m00"])
            centro = largura//2

            erro = cx - centro

            correcao = kp * erro

            vel_esq = vel_base - correcao
            vel_dir = vel_base + correcao

            vel_esq = max(0,min(100,vel_esq))
            vel_dir = max(0,min(100,vel_dir))

            pwm_esq.ChangeDutyCycle(vel_esq)
            pwm_dir.ChangeDutyCycle(vel_dir)

        else:

            # perdeu pista
            pwm_esq.ChangeDutyCycle(0)
            pwm_dir.ChangeDutyCycle(0)

        cv2.imshow("Visao",img)
        cv2.imshow("Mascara",mascara)

        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrompido")

finally:

    print("Encerrando")

    pwm_esq.stop()
    pwm_dir.stop()

    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

    print("Sistema finalizado")