import RPi.GPIO as GPIO
import time

# Configuración del pin del botón
button_pin = 23  # Cambia este número si usas otro pin GPIO

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Botón con resistencia pull-up interna

def button_pressed(channel):
    print("¡Botón presionado!")

# Configurar la detección de eventos para el botón
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed, bouncetime=300)  # Debounce time = 300ms

try:
    print("Probando el botón. Presiona el botón para ver si funciona...")
    while True:
        time.sleep(1)  # Mantener el script en ejecución

except KeyboardInterrupt:
    print("Prueba terminada por el usuario.")

finally:
    GPIO.cleanup()  # Limpiar los recursos de GPIO
    print("GPIO limpiado.")
