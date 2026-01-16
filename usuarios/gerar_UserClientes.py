import hashlib
from faker import Faker

fake = Faker('pt_BR')


def make_django_password(raw_password):
    salt = fake.lexify(text='????????????????')
    hash_ = hashlib.pbkdf2_hmac(
        'sha256', raw_password.encode(), salt.encode(), 260000)
    return f"pbkdf2_sha256$260000${salt}${hash_.hex()}"


def gerar_usuarios_sql(qtd=100, senha='UNIVESP'):
    with open("novosUsers.sql", "w", encoding="utf-8") as f:
        f.write("INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)\nVALUES\n")

        valores = []
        for _ in range(qtd):
            username = fake.user_name()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password_hash = make_django_password(senha)

            valor = f"('{password_hash}', NULL, 0, '{username}', '{first_name}', '{last_name}', '{email}', 0, 1, CURRENT_TIMESTAMP)"
            valores.append(valor)

        f.write(",\n".join(valores) + ";\n")


gerar_usuarios_sql()
