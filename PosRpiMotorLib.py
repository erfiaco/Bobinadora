from RpiMotorLib import RpiMotorLib
import Adafruit_ADS1x15
import time
import RPi.GPIO as GPIO

#Pin Configuration GPIO mode
step_pin_pos = 17
dir_pin_pos = 18

#creo instancia del motor
posicionador = RpiMotorLib.A4988Nema(dir_pin_pos, step_pin_pos,(5,6,13), "A4988")

#configuracion del posicionador
steps_per_revolution_pos = 200

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


positions = [400,20,1,5,6,8]

movements = generate_steps_matrix(positions)
        

try:
    vueltas = len(positions)+1
    i = 0

    while i < vueltas and running:
  
        #mover motor a posicion determinada
        posicionador.motor_go(movements[i][1], "Full", movements[i][0], 0.001, False, 1/speed)
  
        i += 1
        
