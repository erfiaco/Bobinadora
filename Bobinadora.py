from RpiMotorLib import RpiMotorLib
import Adafruit_ADS1x15
import time
import RPi.GPIO as GPIO

#Pin Configuration GPIO mode
step_pin = 17
dir_pin = 18
button_pin = 23

#creo instancia del motor
stepper = RpiMotorLib.A4988Nema(dir_pin, step_pin,(5,6,13), "DRV8825")
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

#configuracion del motor
min_speed = 200 #pasos por segundo
max_speed = 1000 #pasos por segundo
steps_per_revolution = 200 #200 pasos x 4 (microstepping)

# Global flag loop control
running = True

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor


def map_value(value, in_min, in_max, out_min, out_max):
    return(value-in_min)*(out_max-out_min)/(in_max -in_min) + out_min

def stop_loop(channel):
    global running
    print("Button pressed. Stopping the loop...")
    running = False

# Add event detector for the button
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=stop_loop, bouncetime=300)  # Debounce time = 300ms


try:
    vueltas = 10
    i = 0

    while i < vueltas and running:
  
        #leer valor potenciometro
        pot_value = adc.read_adc(0, gain = GAIN)
        #mapear valor del potenciometro a la vel del motor
        speed = map_value(pot_value, 0, 32767, min_speed, max_speed)
  
        #mover motor a vel calculada
        stepper.motor_go(True, "Full", steps_per_revolution, 1.0 / speed, False, 0)
  
        i += 1
        print(f"N. de vueltas: {i}, a vel: {speed/steps_per_revolution} vueltas/seg")  
  

except KeyboardInterrupt:
    print('Programa detenido por el usuario')
    running = False #Ensure the loop stops

finally:
    GPIO.remove_event_detect(button_pin)  # Detener la deteccion de eventos
    stepper.motor_stop()
    GPIO.cleanup()
    print('Motor detenido')
