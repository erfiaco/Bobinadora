import Adafruit_ADS1x15
import time
import smbus2

bus = smbus2.SMBus(1)
address = 0x48

# Configuracion del ADS1115
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1  # Ajusta la ganancia segun el rango de voltaje que estas midiendo

print('Pulse Ctrl + C para finalizar')

try:
    while True:
        # Lee el valor del canal 0 (A0)
        values = adc.read_adc(0, gain=GAIN)
        
        # Convierte el valor a voltaje (opcional)
        voltage = (values * 4.096) / 32767  # 32767 es el valor maximo para 16 bits
        
        # Imprime el valor leido y el voltaje calculado
        print('Valor leido: {0:>6} | Voltaje: {1:.3f} V'.format(values, voltage))
        
        # Espera 0.5 segundos antes de la siguiente lectura
        time.sleep(0.5)

except KeyboardInterrupt:
    print('\nFin del programa.')
