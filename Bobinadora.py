from RpiMotorLib import RpiMotorLib
import Adafruit_ADS1x15
import time

import RPi.GPIO as GPIO

step_pin = 17
dir_pin = 18

#creo instancia del motor
stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin,(5,6,13), "DRV8825")
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

#configuracion del motor
min_speed = 200 #pasos por segundo
max_speed = 1000 #pasos por segundo
steps_per_revolution = 200 #200 pasos x 4 (microstepping)

def map_value(value, in_min, in_max, out_min, out_max):
    return(value-in_min)*(out_max-out_min)/(in_max -in_min) + out_min

try:
    vueltas = 10
    i = 0

    while i < vueltas:
  
        #leer valor potenciometro
        pot_value = adc.read_adc(0, gain = GAIN)
        #mapear valor del potenciometro a la vel del motor
        speed = map_value(pot_value, 0, 32767, min_speed, max_speed)
  
        #mover motor a vel calculada
        stepper.motor_go(True, "Half", steps_per_revolution, 1.0 / speed, False, 0)
  
        i += 1
        print(f"N. de vueltas: {i}, a vel: {speed/steps_per_revolution} vueltas/seg")
  
  

except KeyboardInterrupt:
    print('Programa detenido por el usuario')
    
finally:
    stepper.motor_stop()
    GPIO.cleanup()
    print('Motor detenido')
