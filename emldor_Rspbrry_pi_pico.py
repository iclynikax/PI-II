import requests
import random
import time
from datetime import datetime

url = "http://192.168.1.160:9090/emulador/Rspbrry_PI_Pico_W/emulador/dados/1/"
#                                Rspbrry_PI_Pico_W/emulador/dados/

while True:
    temperatura = round(random.uniform(20.0, 30.0), 2)
    ruido = random.randint(40, 90)
    tempo = datetime.now().strftime("%H:%M:%S")

    payload = {"temperatura": temperatura, "ruido": ruido, "tempo": tempo}
    response = requests.post(url, json=payload)

    print("Tempo do Sistema (datetime.now().strftime(H:M:S)):", tempo )

    try:
        print("Enviado:", payload, "Resposta:", response.json())
    except Exception:
        print("Enviado:", payload, "Resposta bruta:", response.text)

    time.sleep(2)
