
from RpiMotorLib import RpiMotorLib
import time

import RPi.GPIO as GPIO

step_pin = 17
dir_pin = 18

#creo instancia del motor
stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin,(5,6,13), "DRV8825")

#configuracion del motor
speed = 1000 #pasos por segundo
steps_per_revolution = 200 #200 pasos x 4 (microstepping)

'''
try:
  print('Moviendo motor a vel constante, ctrl + c para detener el motor')
  while True:
    stepper.motor_go(True, "Full", steps_per_revolution, 1.0 / speed, True, 0)
    time.sleep(1)
'''

stepper.motor_go(True, "Half", 2*steps_per_revolution, 1.0 / speed, True, 0)

GPIO.cleanup()


'''
except KeyboardInterrupt:
  print('Programa detenido por el usuario')

finally:
  stepper.motor_stop()
  print('Motor detenido')
'''
