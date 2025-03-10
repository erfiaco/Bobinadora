
from RpiMotorLib import RpiMotorLib
import time

step_pin = 17
dir_pin = 18

#creo instancia del motor
stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin,(5,6,13), "DRV8825")

#configuracion del motor
speed = 4000 #pasos por segundo
steps_per_revolution = 800 #200 pasos x 4 (microstepping)

try:
  print('Moviendo motor a vel constante, ctrl + c para detener el motor')
  while True:
    stepper.motor_go(True, "Full", steps_per_revolution, 1.0 / speed, True, 0)
    time.sleep(1)

except KeyboardInterrupt:
  print('Programa detenido por el usuario')

finally:
  stepper.motor_stop()
  print('Motor detenido')
