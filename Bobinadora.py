from RPiMotorLib import RpiMotorLib
import time

step_pin = 17
dir_pin = 18

#creo instancia del motor
Stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin,(21,21,21), "DRV8825")

#configuración del motor
speed = 4000 (pasos por segundo)
steps_per_revolution = 800 #200 pasos x 4 (microstepping)

try:
  print('Moviendo motor a vel constante, ctrl + c para detener el motor')
  while True:
    stepper.motor_go(True, "Full", steps_per_revolution, 1/speed, True, 0)

except KeyboardInterrupt:
  print('Programa detenido por el usuario')

finally:
  stepper.motor_stop()
  print('Motor detenido')
