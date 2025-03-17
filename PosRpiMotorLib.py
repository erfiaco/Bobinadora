from RpiMotorLib import RpiMotorLib
import Adafruit_ADS1x15
import time
import RPi.GPIO as GPIO

#Pin Configuration GPIO mode
step_pin = 17
dir_pin = 18
button_pin = 23

#creo instancia del motor
stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin,(5,6,13), "A4988")

#configuracion del motor
steps_per_revolution = 200 #200 pasos x 4 (microstepping)

# Global flag loop control
running = True

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor

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
speed = 2

positions = [400,20,1,5,6,8]

movements = generate_steps_matrix(positions)
        

        # Ejecutar los movimientos en el vector
        for steps, direction in movements:
            print(f"Moviendo {steps} pasos hacia {direction}...")
            current_t = time.time()
            motor.move_steps(steps, direction)
            elapsed_time = time.time() - current_t
            time.sleep(1 - elapsed_time)  # Esperar el tiempo restante
            

try:
    vueltas = len(positions)+1
    i = 0

    while i < vueltas and running:
  
        #mover motor a posicion determinada
        stepper.motor_go(movements[i][1], "Full", movements[i][0], 0.001, False, 1/speed)
  
        i += 1
          
  

except KeyboardInterrupt:
    print('Programa detenido por el usuario')
    running = False #Ensure the loop stops

finally:
    GPIO.remove_event_detect(button_pin)  # Detener la deteccion de eventos
    stepper.motor_stop()
    GPIO.cleanup()
    print('Motor detenido')
