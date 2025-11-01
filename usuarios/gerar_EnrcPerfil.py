import random
import requests
from faker import Faker

fake = Faker('pt_BR')

# Simulação de IDs existentes
uf_ids = {'SP': 1}  # ajuste conforme seus dados reais


def get_cep_data(prefixo):
    while True:
        cep = f"{prefixo}{random.randint(0, 999):03d}"
        # response = requests.get(f"https://brasilcep.dev/v1/{cep}.json")
        response = requests.get(f'https://brasilapi.com.br/api/cep/v1/{cep}')
        if response.status_code == 200:
            data = response.json()
            if 'cep' in data and 'bairro' in data and 'localidade' in data and 'uf' in data:
                return data


def gerar_sql(qtd_usuarios=250):
    with open("novosPerfil.sql", "w", encoding="utf-8") as f:
        for _ in range(qtd_usuarios):
            user_id = random.randint(23, 123)  # ID aleatório entre 23 e 123
            perfis_por_user = random.randint(3, 5)
            for _ in range(perfis_por_user):
                cep_data = get_cep_data(random.choice(['17800', '17780']))
                endereco = fake.street_address().replace("'", "''")
                bairro = cep_data['bairro'].replace("'", "''")
                cidade = cep_data['localidade'].replace("'", "''")
                uf_id = uf_ids.get(cep_data['uf'], 'NULL')
                celular = fake.msisdn()[:11]
                fixo = fake.msisdn()[:11]
                rg = f"rgs/{fake.file_name(extension='jpg')}"
                cpf = fake.cpf()
                foto = f"fotos_perfil/{fake.file_name(extension='jpg')}"
                descricao = fake.text(max_nb_chars=200).replace("'", "''")
                empresa = fake.company().replace("'", "''")
                cargo = fake.job().replace("'", "''")
                token = fake.uuid4()

                sql = f"""
INSERT INTO seu_app_perfil (user_id, Endereco, Bairro, Cidade, Country, UF_id, CEP, Celular, TelFixo, RG, CPF, Foto, Descricao, Empresa, Cargo, token)
VALUES ({user_id}, '{endereco}', '{bairro}', '{cidade}', 'Brasil', {uf_id}, '{cep_data['cep']}', '{celular}', '{fixo}', '{rg}', '{cpf}', '{foto}', '{descricao}', '{empresa}', '{cargo}', '{token}');
"""
                f.write(sql)


gerar_sql()
