from RpiMotorLib import RpiMotorLib
import Adafruit_ADS1x15
import time
import RPi.GPIO as GPIO
import threading
import LCD_I2C_classe as LCD

lcd = LCD.LCD_I2C()

#Pin Configuration GPIO mode
step_pin = 17
dir_pin = 18
button_pin = 23
step_pin_pos = 16  #Board 36
dir_pin_pos = 20  #Board 38

#creo instancia del motor
stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin, (5, 6, 13), "DRV8825")
posicionador = RpiMotorLib.A4988Nema(dir_pin_pos, step_pin_pos, (21, 21, 21), "DRV8825")  #el motor es de 5v

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

#configuracion del motor
min_speed = 10  #pasos por segundo
max_speed = 400  #pasos por segundo
steps_per_revolution = 200  #200 pasos x 4 (microstepping)

# Global flag loop control
running = True

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def stop_loop(channel):
    global running
    print("Button pressed. Stopping the loop...")
    running = False


# Filtro de promedio movil
readings = []
num_readings = 3  # Numero de lecturas para el promedio


def read_potentiometer():
    global readings
    pot_value = adc.read_adc(0, gain=GAIN)
    readings.append(pot_value)
    if len(readings) > num_readings:
        readings.pop(0)
    return sum(readings) / len(readings)


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


def mover_stepper(steps, speed):
    """ Función para mover el motor principal en un hilo """
    stepper.motor_go(True, "Full", steps, 1.0 / speed, False, 0)


def mover_posicionador(steps, direction, speed):
    """ Función para mover el posicionador en un hilo """
    posicionador.motor_go(direction, "Full", steps, 0.001, False, steps_per_revolution / speed - 0.001 * steps)


try:
    vueltas = 10
    i = 0

    while i < vueltas and running:
        #leer valor potenciometro
        pot_value = read_potentiometer()
        #mapear valor del potenciometro a la vel del motor
        #speed = map_value(pot_value, 0, 32767, min_speed, max_speed)
        speed = 200 #inutilizamos el potenciómetro hasta que no arreglemos sus problemas

        # Crear hilos para cada motor
        thread_stepper = threading.Thread(target=mover_stepper, args=(steps_per_revolution, speed))
        thread_posicionador = threading.Thread(target=mover_posicionador, args=(movements[i][0], movements[i][1], speed))

        # Iniciar los hilos
        thread_stepper.start()
        thread_posicionador.start()
        lcd.write(f"N. de vueltas: {i}, a vel: {speed / steps_per_revolution} vueltas/seg", 1)
        # Esperar a que ambos motores terminen
        thread_stepper.join()
        thread_posicionador.join()

        i += 1
        print(f"N. de vueltas: {i}, a vel: {speed / steps_per_revolution} vueltas/seg")



except KeyboardInterrupt:
    print('Programa detenido por el usuario')
    running = False  #Ensure the loop stops

finally:
    GPIO.remove_event_detect(button_pin)  # Detener la deteccion de eventos
    stepper.motor_stop()
    posicionador.motor_stop()
    GPIO.cleanup()
    lcd.clear()
    print('Motor detenido')
