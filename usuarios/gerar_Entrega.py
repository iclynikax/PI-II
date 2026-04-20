from datetime import datetime, timedelta
import requests
import time

# parâmetros
acoes = ['R', 'E']
status = ['A', 'I', 'F', 'C']
localizacoes = [
    "Rua Deputado Salles Filho, 469 - Centro, Adamantina/SP - 17800-959",
]

observacoes = [
    "Retirada concluída com sucesso",
    "Entrega agendada",
    "Retirada realizada",
    "Entrega em andamento",
    "Retirada finalizada",
    "Entrega cancelada pelo cliente"
]

# Função para geocodificar com Nominatim
def geocodificar(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": endereco, "format": "json"}
    response = requests.get(url, params=params, headers={"User-Agent": "gera_inserts_script"})
    data = response.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None


# Gera lista de coordenadas para cada endereço
coordenadas = []
for loc in localizacoes:
    lat, lon = geocodificar(loc)
    coordenadas.append((lat, lon))
    time.sleep(1)  # respeitar limite de requisições do Nominatim



    

inicio = datetime(2025, 1, 10, 10, 0)
linhas = []

for i in range(100):
    acao = acoes[i % 2]
    stat = status[i % 4]
    pet = (i % 10) + 1
    cliente = (i % 2) + 1
    usuario = (i % 3) + 1
    link = f"https://maps.app.goo.gl/abc{str(i+1).zfill(3)}"
    loc = localizacoes[i % len(localizacoes)]
    lat, lng = coordenadas[i % len(coordenadas)]
    obs = observacoes[i % len(observacoes)]

    abertura = inicio + timedelta(days=i, minutes=i)
    fechamento = None if stat in ['A','I','C'] else abertura + timedelta(hours=1, minutes=15)

    abertura_str = abertura.strftime("%Y-%m-%d %H:%M:%S")
    fechamento_str = f"'{fechamento.strftime('%Y-%m-%d %H:%M:%S')}'" if fechamento else "NULL"

    linha = f"('{acao}','{abertura_str}',{fechamento_str},'{stat}','{link}','{loc}',{lat},{lng},'{obs}',{pet},{cliente},{usuario})"
    linhas.append(linha)

sql = "INSERT INTO paciente_entregaretirada\n" \
      "(acao, data_abertura, data_fechamento, status, link, localizacao, latitude, longitude, observacoes, Pet_Cliente_id, cliente_id, usuario_responsavel_id)\n" \
      "VALUES\n" + ",\n".join(linhas) + ";"

with open("entregaretirada.sql", "w", encoding="utf-8") as f:
    f.write(sql)

print("Arquivo entregaretirada.sql gerado com 100 registros.")
