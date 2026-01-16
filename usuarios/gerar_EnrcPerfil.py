import random
import requests
from faker import Faker
import uuid
from brazilcep import get_address_from_cep

fake = Faker('pt_BR')

# Simulação de IDs existentes
uf_ids = {'SP': 25}  # ajuste conforme seus dados reais


def get_cep_data(prefixo):
    while True:
        cep = f"{prefixo}{random.randint(0, 999):03d}"
      # response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
      # url = f'https://brasilapi.com.br/api/cep/v1/{cep}'
      # resultado = buscar_Endereco(url, cep)

        # Constrói o link de acesso à API ViaCEP
        # link = f'https://viacep.com.br/ws/{cep}/json/'
        link = f'https://brasilapi.com.br/api/cep/v1/{cep}'

        # Realiza a requisição GET para obter os dados do CEP
        # requisicao = requests.get(link)
        # resultado = buscar_Endereco(url, cep)
        # requisicao = get_address_from_cep(cep)
        requisicao = requests.get(link)

        print(
            f'response:{requisicao} - CEP:{cep}  |  requisicao.status_code:[{requisicao.status_code}] ')

        if requisicao.status_code == 200:
            data = requisicao.json()

            print(f'data:{data}')

            if 'cep' in data and 'neighborhood' in data and 'city' in data and 'state' in data and not data.get('erro'):
                print(
                    f'cep:{cep} - bairro: {data['neighborhood']} - localidade:{data['city']}   |  uf:{data['state']}  = {data.get('erro')}')
                return {
                    'cep': data['cep'],
                    'bairro': data['neighborhood'],
                    'localidade': data['city'],
                    'uf': data['state']
                }


def gerar_sql(qtd_usuarios=100):
    with open("novosPerfil.sql", "w", encoding="utf-8") as f:
        f.write("INSERT INTO usuarios_perfil (user_id, Endereco, Bairro, Cidade, Country, UF_id, CEP, Celular, TelFixo, RG, CPF, Foto, Descricao, Empresa, Cargo)\nVALUES\n")

        valores = []
        # IDs únicos entre 23 e 123
        user_ids = random.sample(range(23, 124), qtd_usuarios)

        print(f'user_ids:{user_ids}')

        for user_id in user_ids:
            print(f'user_ids:{user_ids} - user_id:{user_id}')

            cep_data = get_cep_data(random.choice(['17800', '17780']))

            print(f'cep_data:{cep_data}')

            endereco = fake.street_address().replace("'", "''")
            bairro = cep_data['bairro'].replace("'", "''")
            cidade = cep_data['localidade'].replace("'", "''")
            uf_id = uf_ids.get(cep_data['uf'], 'NULL')
            celular = fake.msisdn()[:11]
            fixo = fake.msisdn()[:11]
            rg = f"rgs/{fake.file_name(extension='jpg')}"
            cpf = fake.cpf()
            foto = f"fotos_perfil/{fake.file_name(extension='jpg')}"
            descricao = fake.text(max_nb_chars=100).replace("'", "''")
            empresa = fake.company().replace("'", "''")
            cargo = fake.job().replace("'", "''")

            valor = f"({user_id}, '{endereco}', '{bairro}', '{cidade}', 'Brasil', {uf_id}, '{cep_data['cep']}', '{celular}', '{fixo}', '{rg}', '{cpf}', '{foto}', '{descricao}', '{empresa}', '{cargo}')"

            print(f'----------------------------------Valor: {valor}')

            valores.append(valor)

        f.write(",\n".join(valores) + ";\n")


gerar_sql()
