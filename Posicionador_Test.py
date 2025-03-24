from RpiMotorLib import RpiMotorLib
import Adafruit_ADS1x15
import time
import RPi.GPIO as GPIO

# Pin Configuration GPIO mode

button_pin = 23
step_pin_pos = 6  # Board 31
dir_pin_pos = 12  # Board 32

# creo instancia del motor
posicionador = RpiMotorLib.A4988Nema(dir_pin_pos, step_pin_pos, (21, 21, 21), "DRV8825")  # el motor es de 5v

# Global flag loop control
running = True

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor


def stop_loop(channel):
    global running
    print("Button pressed. Stopping the loop...")
    running = False

def generate_steps_matrix(positions):
    """
    Genera una matriz con el número de pasos necesarios y la dirección para alcanzar
    cada posición objetivo desde la posición actual.

    :param positions: Lista de posiciones en el eje X.
    :return: Lista de listas (matriz) con pasos y direcciones.
    """
    current_position = 0
    steps_matrix = []

    for target_position in positions:
        steps = abs(target_position - current_position)
        direction = True if target_position > current_position else False
        steps_matrix.append([steps, direction])
        current_position = target_position  # Actualiza la posición actual

    return steps_matrix


# Add event detector for the button
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=stop_loop, bouncetime=300)  # Debounce time = 300ms

positions = [400, 20, 1, 5, 6, 8]
movements = generate_steps_matrix(positions)

try:
    vueltas = 10
    i = 0

    while i < vueltas and running:

        speed = 1000

        # mover motor posicionador hasta alcanzar posicion deseada
        posicionador.motor_go(movements[i][1], "Full", movements[i][0], 0.001, False, steps_per_revolution / speed - 0.001 * movements[i][1])

        i += 1
        print(f"N. de vueltas: {i}, a vel: {speed / steps_per_revolution} vueltas/seg")


except KeyboardInterrupt:
    print('Programa detenido por el usuario')
    running = False  # Ensure the loop stops

finally:
    GPIO.remove_event_detect(button_pin)  # Detener la deteccion de eventos
    stepper.motor_stop()
    posicionador.motor_stop()
    GPIO.cleanup()
    print('Motor detenido')
