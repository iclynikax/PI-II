from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now, make_aware, localtime
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Count, DateTimeField
from datetime import datetime
from paciente.models import PetLocalAssignment, PetMonitorHistory
from django.views.decorators.csrf import csrf_exempt
import os
import json
import random
import subprocess 
'''    módulo do Python voltado para criar e gerenciar processos.
       Com ele você inicia um programa externo (Popen), pode capturar saída, enviar entrada, e encerrar com métodos como .terminate() ou .kill().
       Esses métodos são mais simples:
       .terminate() envia um sinal de término padrão (no Linux é SIGTERM).
       .kill() envia um sinal de morte imediata (SIGKILL).
       Ou seja, com subprocess você controla o ciclo de vida básico do processo: iniciar e encerrar.'''

import signal
from django.http import JsonResponse


@login_required(login_url='/usuarios/login/')
def home(request):
    # Simula valores de temperatura e ruído
    temperatura = round(random.uniform(20, 30), 2)
    ruido = random.randint(40, 90)
    tempo = datetime.now().strftime("%H:%M:%S")
    id_assignment = request.id
    if request.method == "GET":
        iframe_url = f"ESP32_S3.html?temperatura={temperatura}&ruido={ruido}&tempo={tempo}&nId_assignment={id_assignment}"
        return render(request, 'index.html', {
                     'iframe_ESP32_S3_url': iframe_url,
                        }
                      )


@login_required(login_url='/usuarios/login/')
def fnctn_esp32_s3(request):
    if request.method == "GET":
        # Simula valores de temperatura e ruído
        temperatura = round(random.uniform(20, 30), 2)
        ruido = random.randint(40, 90)
        tempo = datetime.now().strftime("%H:%M:%S")

        return render(request, "ESP32_S3.html", {
            "temperatura": temperatura,
            "ruido": ruido,
            "tempo": tempo,
            'rtrds_mntrmnto': request
        })
    


def fnctn_emulador_esp32_s3(request, id_Mntoramento):
    return render(request, "ESP32_S3_Chart.html", {"id_assignment":id_Mntoramento} )


# A função está atuando como o endpoint que gera os dados de temperatura e
# ruído e os retorna em formato JSON para o frontend.
def fnctn_dados_esp32_s3(request, id_assignment):
    temperatura = round(random.uniform(20, 30), 2)
    ruido = random.randint(40, 90)
    tempo = datetime.now().strftime("%H:%M:%S")    

    # Recupera o assignment (pet em local)
    assignment = PetLocalAssignment.objects.get(id=id_assignment)

    # # Salva a leitura do ruido e da temperatura no banco de dados
    PetMonitorHistory.objects.create(
        assignment=assignment,
        temperature=temperatura,
        noise=ruido
    )
    # Retorna para o frontend
    return JsonResponse({
        "temperatura": temperatura,
        "ruido": ruido,
        "tempo": tempo,
        "timestamp": now().isoformat()
    })





def fnctn_Rspbrry_PI_Pico_W(request, id_Mntoramento):
    if request.method == "GET":
        # Simula valores de temperatura e ruído
        temperatura = round(random.uniform(20, 30), 2)
        ruido = random.randint(40, 90)
        tempo = datetime.now().strftime("%H:%M:%S")

        return render(request, "RSPBRY_PI_WiFi.html", {
            "temperatura": temperatura,
            "ruido": ruido,
            "tempo": tempo,
            'rtrds_mntrmnto': request
        })
    



@login_required(login_url='/usuarios/login/')
def fnctn_emulador_Rspbrry_PI_Pico_W(request, id_Mntoramento):
    return render(request, "RSPBRY_PI_WiFi_Chart.html", {"id_assignment":id_Mntoramento} )



# A função está atuando como o endpoint que gera os dados de temperatura e
# ruído e os retorna em formato JSON para o frontend.

# variável global para guardar último dado recebido
ultimo_dado = {}

@csrf_exempt
def fnctn_dados_Rspbrry_PI_Pico_W(request, id_assignment):
    global ultimo_dado

    if request.method == "POST":
        dados = json.loads(request.body.decode("utf-8"))
        ultimo_dado = {
            "temperatura": dados.get("temperatura"),
            "ruido": dados.get("ruido"),
            "tempo": dados.get("tempo"),
        }
        return JsonResponse({"status": "ok"})

    elif request.method == "GET":
        if ultimo_dado:
            return JsonResponse(ultimo_dado)
        return JsonResponse({"erro": "nenhum dado recebido ainda"})

    return JsonResponse({"erro": "Método não permitido"})



# Observação: o exemplo usa lwIP + http_client para enviar dados. 
# Na prática, você precisa configurar corretamente o cliente HTTP da biblioteca lwIP.
@csrf_exempt
def fnctn_rspbrry_PI_Pico(request, id_assignment):
    if request.method == "POST":
        dados = json.loads(request.body.decode("utf-8"))
        temperatura = dados.get("temperatura")
        ruido = dados.get("ruido")

        return JsonResponse({
            "status": "ok",
            "id_assignment": id_assignment,
            "temperatura": temperatura,
            "ruido": ruido
        })
    return JsonResponse({"status": "erro", "mensagem": "Método não permitido"})


# variável global para guardar o processo -------------------------------------------------------------------------------------------------------------
processo_emulador = None

@csrf_exempt
def fnctn_start_emldr_rspbrry_PI_Pico(request):
    global processo_emulador
    if not processo_emulador:  # só inicia se não houver processo rodando
        processo_emulador = subprocess.Popen(["python", "emulador_pico.py"])
        return JsonResponse({"status": "emulador iniciado"})
    else:
        return JsonResponse({"status": "já existe um emulador em execução"})

@csrf_exempt
def fnctn_pause_emldr_rspbrry_PI_Pico(request):
    global processo_emulador
    if processo_emulador:
        os.kill(processo_emulador.pid, signal.SIGSTOP)  # pausa o processo
        return JsonResponse({"status": "emulador pausado"})
    else:
        return JsonResponse({"status": "nenhum emulador em execução"})

@csrf_exempt
def fnctn_resume_emldr_rspbrry_PI_Pico(request):
    global processo_emulador
    if processo_emulador:
        os.kill(processo_emulador.pid, signal.SIGCONT)  # retoma o processo
        return JsonResponse({"status": "emulador retomado"})
    else:
        return JsonResponse({"status": "nenhum emulador em execução"})

@csrf_exempt
def fnctn_stop_emldr_rspbrry_PI_Pico(request):
    global processo_emulador
    if processo_emulador:
        processo_emulador.terminate()  # encerra o processo definitivamente
        processo_emulador = None
        return JsonResponse({"status": "emulador finalizado"})
    else:
        return JsonResponse({"status": "nenhum emulador em execução"})
