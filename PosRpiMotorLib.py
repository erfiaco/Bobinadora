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

Posiciones = [400,20,1,5,6,8]



try:
    vueltas = 10
    i = 0

    while i < vueltas and running:
  
        #leer valor potenciometro
        pot_value = read_potentiometer()
        #mapear valor del potenciometro a la vel del motor
        speed = map_value(pot_value, 0, 32767, min_speed, max_speed)
  
        #mover motor a posicion determinada
        stepper.motor_go(True, "Full", steps_per_revolution, 0.001, False, 1/speed)
  
        i += 1
          
  

except KeyboardInterrupt:
    print('Programa detenido por el usuario')
    running = False #Ensure the loop stops

finally:
    GPIO.remove_event_detect(button_pin)  # Detener la deteccion de eventos
    stepper.motor_stop()
    GPIO.cleanup()
    print('Motor detenido')
