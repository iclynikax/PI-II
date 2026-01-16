from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from usuarios.models import Get_cGrp_Usuario
from usuarios.models import Prfl_Endereco
from paciente.models import Pet_Cliente
from paciente.models import Pet
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import requests
import json       # Usado para salvar o status no menu esquerdo para o Usuário
from django.contrib.auth.forms import PasswordChangeForm
from brazilcep import get_address_from_cep

from django.conf import settings
from django.urls import reverse

from medico.models import is_medico
from . models import Perfil, UfEstados

import smtplib
import email.message

import os
from PIL import Image

import uuid


# -----------------------------------------------------------------------------------------------
# Realiza a busca do cep informado.
def buscar_endereco(request, cep):
    url = f'https://brasilapi.com.br/api/cep/v1/{cep}'
    response = requests.get(url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'CEP não encontrado'}, status=404)

# Exemplo de uso
# cep = "77006388"
# url = f'https://brasilapi.com.br/api/cep/v1/{cep}'
# resultado = buscar_Endereco(url, cep)
# print(resultado)

# ---------------------------------------------------------------------------------
# Realiza a Busca do CEP Informado via API BrasilCEP
# ---------------------------------------------------------------------------------


def buscar_endereco_com_brazilcep(cep):
    try:
        endereco = get_address_from_cep(cep)
        return endereco
    except Exception as e:
        return {"erro": "Não foi possível buscar o endereço.", "detalhes": str(e)}
# ---------------------------------------------------------------------------------


def seek_endereco_com_brazilcep(cep):

    # Constrói o link de acesso à API ViaCEP
    link = f'https://viacep.com.br/ws/{cep}/json/'

    # Realiza a requisição GET para obter os dados do CEP
    requisicao = requests.get(link)

    # Verifica se a requisição foi bem-sucedida (código de resposta 200)
    if requisicao.status_code == 200:
        # Converte os dados da resposta para um dicionário
        dados_cep = requisicao.json()

        # Extrai e exibe as informações do CEP
        uf = dados_cep.get('uf')
        cidade = dados_cep.get('localidade')
        bairro = dados_cep.get('bairro')
        endereco = dados_cep.get('logradouro')

        # Exibe as informações
        print(f'Estado (UF): {uf}')
        print(f'Cidade: {cidade}')
        print(f'Bairro: {bairro}')
        print(f'Endereço: {endereco}')
    else:
        print(f'Erro ao consultar o CEP: código {requisicao.status_code}')

# Exemplo de uso
# cep = "77006-388"
# resultado = seek_endereco_com_brazilcep(cep)
# -----------------------------------------------------------------------------------------------
# Se o email informado estiver no banco de dados, envia um link por eMail.


def fnct_resetar(request):
    if request.method == "GET":
        token = uuid.uuid4()  # Gera um token único
        return render(request, 'resetar_senha.html', {'token': token})

    return render(request, 'resetar_senha.html')

# -----------------------------------------------------------------------------------------------
# Atualiza a senha do usuário.


def fnct_upgrde_snha(request, token):
    if request.method == "POST":
        slct_id_Perfil = Perfil.objects.get(token=token)
        updte_Usario = User.objects.get(id=slct_id_Perfil.user_id)

        get_snha_001 = request.POST.get("getsenha1")
        get_snha_002 = request.POST.get("getsenha2")

        if (get_snha_001 != get_snha_002):
            messages.add_message(request, constants.ERROR,
                                 'A senhas digitada não são iguais. A Senha e o confirmar senha devem ser iguais...')
            return redirect(f'../redefinindo/{token}')

        if len(get_snha_001) < 6:
            messages.add_message(request, constants.ERROR,
                                 'A senha deve possuir pelo menos 6 caracteres')
            return redirect(f'../redefinindo/{token}')

        if (get_snha_001 == get_snha_002):
            updte_Usario.set_password(get_snha_001)
            updte_Usario.save()

            messages.add_message(request, constants.INFO,
                                 'Sua senha foi alterada com sucesso...')
            return redirect('/usuarios/login')
        else:
            messages.add_message(request, constants.INFO,
                                 'A senha informada não são iguais')
            return redirect('/usuarios/login')

    return redirect('/usuarios/login')


def fnct_enviar_email_restar_senha(request):
    if request.method == "GET":
        return render(request, 'resetar_senha.html')

    elif request.method == "POST":
        Slct_get_email = request.POST.get("get_email")
        user = User.objects.filter(email=Slct_get_email)

        if user.exists():

            usuario = get_object_or_404(user, email=Slct_get_email)

            Perfil_User = Perfil.objects.get(user=usuario.id)

            token = uuid.uuid4()
            # Supondo que você tenha um campo 'token' no perfil do usuário
            Perfil_User.token = token
            Perfil_User.save()

            # cLink = "rfzndo_senha.html"
            cLink = "http://construplus.net:9090/usuarios/redefinindo/"
            cLink += f"{token}"

            # return render(request, 'clientes_lista.html', {'RlcaoDClntes': slct_Clnts_Lsta})

            # cLink += password_reset_confirm
            # cLink += uidb64=uid token=token %}

            # send_mail('Assunto','Esse é o email de teste de enviar email do Django', 'gdmacedo@gmail.com', ['gdmacedo@hotmail.com'])
            # mensagem  = "Corpo da mensagem principal"
            # email = EmailMessage(subject='Assunto do eMail',
            #                    body='Mensagem Principal',
            #                    from_email=settings.EMAIL_HOST_USER,
            #                    to=['gdmacedo@outlook.com']
            #                    )
            # email.send()

            corpo_email = """
            <p>Você solicitou resetar sua senha de acesso ao nosso ERP.</p>
            <p><b>Username:</b>
            """
            corpo_email += usuario.username
            corpo_email += """<p>
            <p>Click no link abaixo para criar uma nova senha de acesso.</p>
            <p></p>
            <p><b>Link:</b></p>
            """
            corpo_email += cLink
            corpo_email += """<p>
            <p> </p>
            <p> </p>
            <p> </p>
            <p> </p>
            <p> </p>
            <p> </p>
            <p> </p>
            <p> </p>
            <p></p>
            <p>Projeto Integrador I - Polo Adamantina : 2025</p>
            <p></p>
            <p>UNIVESP - Universidade Virtual de São Paulo</p>
            """

            msg = email.message.Message()
            msg['Subject'] = "Redefinindo sua senha."
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = Slct_get_email
            password = settings.EMAIL_HOST_PASSWORD
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']],
                       msg.as_string().encode('iso-8859-1'))

            request.session.flush()
            messages.add_message(
                request, constants.INFO, 'E-mail de redefinição de senha enviado com sucesso. Verifica seu eMail, para resetar sua senha...')
            return redirect('/usuarios/login')

        else:
            print("O email informado não existe!!!")
            messages.add_message(
                request, constants.ERROR, 'O eMail informado não se encontra cadastrado...')
            return redirect('url_resetar')


# -----------------------------------------------------------------------------------------------
# Redefindo a senha após o click no eMail enviado.
def fnct_rdfnndo(request, token):
    if request.method == "GET":
        Perfil_User = Perfil.objects.get(token=token)

        usuario = User.objects.filter(email=Perfil_User.user.email)

        user = auth.authenticate(request, email=Perfil_User.user.email)

        if usuario:
            #           return render(request, 'clientes_lista.html', {'RlcaoDClntes': slct_Clnts_Lsta})
            return render(request, 'rdfndo_senha.html', {'Usuario': Perfil_User})

        else:
            messages.success(request, 'O Token não é valido.')
            return render(request, 'rdfndo_senha.html')

    elif request.method == "POST":
        get_email = request.POST.get('email')

        user = User.objects.filter(email=get_email)

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')


def fnct_cdstro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get('confirmar_senha')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR,
                                 'O Usuário já esta cadastrado...')
            return redirect('/usuarios/cadastro')

        if senha != confirmar_senha:
            messages.add_message(
                request, constants.ERROR, 'A senhas digitada não são iguais. A Senha e o confirmar senha devem ser iguais...')
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/usuarios/cadastro')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )

            return redirect('/usuarios/login')
        except:
            print('Erro 4')
            return redirect('/usuarios/cadastro')


@login_required(login_url='/usuarios/login/')
def fnct_clnts_lista(request):

    slct_Clnts_Lsta = User.objects.all().filter(is_superuser=0)

    return render(request, 'clientes_lista.html', {'RlcaoDClntes': slct_Clnts_Lsta, 'cGrp_Usuario': Get_cGrp_Usuario(request.user)})


@login_required(login_url='/usuarios/login/')
def fnct_clnts_edit(request, id_cliente):
    #    if not is_medico(request.user):
    #        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
    #        return redirect('/usuarios/logout')

    if request.method == "GET":
        slct_id_cliente = User.objects.get(id=id_cliente)
        slct_Usario = User.objects.get(id=request.user.id)

    #   slct_id_Perfil = Perfil.objects.get(user=id_cliente)

        try:
            slct_id_Perfil, criado = Perfil.objects.get_or_create(
                user=slct_id_cliente,
                defaults={'Foto': 'fotos_perfil/usuario_sem_foto.png'}
            )
            if criado:
                print("Perfil criado!")

        except Exception as e:
            print("Erro ao criar perfil:", e)

        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        slct_Pet_Sxos = list(Pet_Cliente.Pet_Sexo_Id)

        slct_Get_Pet = Pet.objects.all().order_by(
            'Pet')  # Seleciona todos os Pets

        return render(request, 'cliente.html', {'Lst_Pets': slct_Get_Pet, 'Lst_Pts_Sxo': slct_Pet_Sxos, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

    elif request.method == "POST":
        slct_id_cliente = User.objects.get(id=id_cliente)
        slct_id_Perfil = Perfil.objects.get(user=id_cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        slct_Pet_Sxos = list(Pet_Cliente.Pet_Sexo_Id)

        slct_Get_Pet = Pet.objects.all().order_by(
            'Pet')  # Seleciona todos os Pets

        slct_modo = request.POST.get('get_modo', 'Indefinido').strip()

        updte_first_name = request.POST.get('get_first_nome', '').strip()
        updte_last_name = request.POST.get('get_last_nome', '').strip()

        print(slct_modo)

    if slct_modo == 'Perfil':
        slct_id_cliente.first_name = updte_first_name
        slct_id_cliente.last_name = updte_last_name
        slct_id_cliente.save()

        slct_id_Perfil = Perfil.objects.get(user=id_cliente)
        slct_id_Perfil.Celular = request.POST.get('get_celular')
        slct_id_Perfil.Cargo = request.POST.get('get_cargo')
        slct_id_Perfil.Descricao = request.POST.get('get_descricao')
        slct_id_Perfil.save()

    if slct_modo == 'Endereço':
        slct_id_Perfil = Perfil.objects.get(user=id_cliente)

        slct_id_Perfil.Endereco = request.POST.get('get_endereco')
        slct_id_Perfil.Bairro = request.POST.get('get_bairro')
        slct_id_Perfil.Cidade = request.POST.get('get_cidade')

        uf_id = request.POST.get('get_uf')
        slct_id_Perfil.UF = UfEstados.objects.get(id=int(uf_id))

        slct_id_Perfil.CEP = request.POST.get('get_cep')
        slct_id_Perfil.save()

    slct_Clnts_Lsta = User.objects.all().filter(is_superuser=0)

    if slct_modo == 'Foto_Perfil':
        get_img_foto = request.FILES.get('foto')
        print(get_img_foto)
        try:
            if get_img_foto is not None:

                img_save = Image.open(get_img_foto)
                path = os.path.join(settings.BASE_DIR,
                                    f'media/fotos_perfil/{get_img_foto.name}')
                img_save = img_save.save(path)

                updte_Usario = User.objects.get(id=id_cliente)
                updte_Perfil, criado = Perfil.objects.get_or_create(
                    user=updte_Usario,
                    defaults={'Foto': 'fotos_perfil/usuario_sem_foto.png'}
                )
                if criado:
                    print("Perfil criado!")

                updte_Perfil.Foto = f'fotos_perfil/{get_img_foto.name}'
                updte_Perfil.save()

                print('Salva Foto no Perfil')
                print(get_img_foto)

                messages.add_message(
                    request, constants.SUCCESS, 'A Foto foi salva com sucesso...', 'bi bi-check-circle me-1')

                return redirect('/usuarios/my-profile/')
            else:
                if get_firstname is None:
                    messages.add_message(
                        request, constants.ERROR, 'A Foto não foi informada...')

                    return redirect('/usuarios/my-profile/')

        except:
            print('Erro em Salvar Foto...')
            print(get_img_foto)


#        return render(request, 'clientes_lista.html', {'RlcaoDClntes': slct_Clnts_Lsta, 'Perfil': slct_id_Perfil})

    messages.add_message(request, constants.SUCCESS,
                         'Dados do Cliente cliente salvo com sucesso!')

    return render(request, 'cliente.html', {'Lst_Pets': slct_Get_Pet, 'Lst_Pts_Sxo': slct_Pet_Sxos, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})


@login_required(login_url='/usuarios/login/')
def fnct_endr_clnt_prfl(request, id_endrco):
    #    if not is_medico(request.user):
    #        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
    #        return redirect('/usuarios/logout')

    if request.method == "GET":
        slct_Endr_Cli = Prfl_Endereco.objects.get(id=id_endrco)
        slct_id_cliente = User.objects.get(
            username=slct_Endr_Cli.cliente.username)
        slct_id_Perfil = Perfil.objects.get(user=slct_Endr_Cli.cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        return render(request, 'cliente_endereco.html', {'Endrc_Cli': slct_Endr_Cli, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

    elif request.method == "POST":
        slct_Endr_Cli = Prfl_Endereco.objects.get(id=id_endrco)
        slct_id_cliente = User.objects.get(
            username=slct_Endr_Cli.cliente.username)
        slct_id_Perfil = Perfil.objects.get(user=slct_Endr_Cli.cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        updte_numero = request.POST.get('get_numero')
        updte_referencia = request.POST.get('get_referencia')

        slct_Endr_Cli.Numero = updte_numero
        slct_Endr_Cli.Referencia = updte_referencia
        slct_Endr_Cli.save()

        return render(request, 'cliente_endereco.html', {'Endrc_Cli': slct_Endr_Cli, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})


# --------------------------------------------------------------------------------------------------------------

@login_required(login_url='/usuarios/login/')
def fnct_endr_prfile(request, id_endrco):
    #    if not is_medico(request.user):
    #        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
    #        return redirect('/usuarios/logout')

    if request.method == "GET":
        slct_Endr_Cli = Prfl_Endereco.objects.get(id=id_endrco)
        slct_id_cliente = User.objects.get(
            username=slct_Endr_Cli.cliente.username)
        slct_id_Perfil = Perfil.objects.get(user=slct_Endr_Cli.cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        return render(request, 'My_Endereco.html', {'Endrc_Cli': slct_Endr_Cli, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

    elif request.method == "POST":
        slct_Endr_Cli = Prfl_Endereco.objects.get(id=id_endrco)
        slct_id_cliente = User.objects.get(
            username=slct_Endr_Cli.cliente.username)
        slct_id_Perfil = Perfil.objects.get(user=slct_Endr_Cli.cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        updte_numero = request.POST.get('get_numero')
        updte_referencia = request.POST.get('get_referencia')

        slct_Endr_Cli.Numero = updte_numero
        slct_Endr_Cli.Referencia = updte_referencia
        slct_Endr_Cli.save()

        return render(request, 'My_Endereco.html', {'Endrc_Cli': slct_Endr_Cli, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})


# Adiciona um novo endereço ao cliente.
@login_required(login_url='/usuarios/login/')
def fnct_endereco_clnte_add(request, id_cliente):
    if request.method == "POST":
        slct_id_cliente = User.objects.get(id=id_cliente)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        slct_id_Perfil = Perfil.objects.get(user=id_cliente)

        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)

        add_cep = request.POST.get('say_cep')
        add_numero = request.POST.get('get_numero')
        add_endereco = request.POST.get('get_logradouro')
        add_cmplnto = request.POST.get('get_complemento')
        add_bairro = request.POST.get('get_bairro')
        add_cidade = request.POST.get('get_cidade')
        add_estado = request.POST.get('get_estado')
        add_idUf = int(request.POST.get('get_uf'))
        add_uf = UfEstados.objects.get(id=add_idUf, UfEstados=add_estado)
        add_referencia = request.POST.get('get_referencia')

        # Busca o cep informado seguido do número e do cliente.
        seekCep = Prfl_Endereco.objects.filter(cliente=slct_id_cliente.id,
                                               CEP=add_cep,
                                               Numero=add_numero
                                               )
        # Se a busca acima existir...
        if seekCep.exists():
            messages.add_message(request, constants.ERROR,
                                 'O CEP e o número para esse cliente já existe...')
            print('Acessou aqui 2')
            return render(request, 'cliente.html', {'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

        else:
            print('Acessou aqui 1')

            nvoEndrco = Prfl_Endereco.objects.create(
                cliente=slct_id_cliente,
                CEP=add_cep,
                Numero=add_numero,
                Referencia=add_referencia,
                Complemento=add_cmplnto,
                Endereco=add_endereco,
                Bairro=add_bairro,
                Cidade=add_cidade,
                UF=add_uf,
                Country='Brasil',
                status='A'
            )
            nvoEndrco.save()

            return render(request, 'cliente.html', {'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

        try:
            return render(request, 'cliente.html', {'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})
        except:
            return render(request, 'cliente.html', {'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})


@login_required(login_url='/usuarios/login/')
def fnct_endereco_clnte_cdstro(request, id_endrco):
    if request.method == "POST":
        slct_Endr_Cli = Prfl_Endereco.objects.get(id=id_endrco)
        slct_id_cliente = User.objects.get(
            username=slct_Endr_Cli.cliente.username)
        slct_id_Perfil = Perfil.objects.get(user=slct_Endr_Cli.cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        updte_numero = request.POST.get('get_numero')
        updte_referencia = request.POST.get('get_referencia')
        updte_cep = request.POST.get('get_cep')

        slct_Endr_Cli.Numero = updte_numero
        slct_Endr_Cli.Referencia = updte_referencia
        slct_Endr_Cli.CEP = updte_cep
        slct_Endr_Cli.save()

        return render(request, 'cliente_endereco.html', {'Endrc_Cli': slct_Endr_Cli, 'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})


@login_required(login_url='/usuarios/login/')
def fnct_clnts_edit_PI_I(request, id_cliente):
    #    if not is_medico(request.user):
    #        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
    #        return redirect('/usuarios/logout')

    if request.method == "GET":
        slct_id_cliente = User.objects.get(id=id_cliente)
        slct_id_Perfil = Perfil.objects.get(user=id_cliente)
        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)

        return render(request, 'cliente.html', {'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

    elif request.method == "POST":
        slct_id_cliente = User.objects.get(id=id_cliente)
        slct_id_Perfil = Perfil.objects.get(user=id_cliente)

        updte_first_name = request.POST.get('get_first_nome')
        updte_last_name = request.POST.get('get_last_nome')

        slct_id_cliente.first_name = updte_first_name
        slct_id_cliente.last_name = updte_last_name
        slct_id_cliente.save()

        slct_id_Perfil = Perfil.objects.get(user=id_cliente)
        slct_id_Perfil.Celular = request.POST.get('get_celular')
        slct_id_Perfil.Cargo = request.POST.get('get_cargo')
        slct_id_Perfil.save()

        slct_Clnts_Lsta = User.objects.all().filter(is_superuser=0)
        return render(request, 'clientes_lista.html', {'RlcaoDClntes': slct_Clnts_Lsta, 'Perfil': slct_id_Perfil})

# ------------------------------------------------------------------------------
# Responsável por realizar login de acesso ao sistema
# ------------------------------------------------------------------------------


def fnct_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get("senha")
        user = auth.authenticate(request, 
                                 username=username, 
                                 password=senha)
        if user:
            auth.login(request, user)
            return redirect('/paciente/home')
        messages.add_message(request, constants.ERROR,
                             'Usuário ou senha incorretos')
        return redirect('/usuarios/login')
# ------------------------------------------------------------------------------


def fnct_rcprrusrnme(request):
    if request.method == "GET":
        return render(request, 'rcprrusrnme.html')
    if request.method == "POST":
        get_email = request.POST.get('email')

        user = User.objects.filter(email=get_email)

        if user.exists():

            usuario = get_object_or_404(user, email=get_email)

            # send_mail('Assunto','Esse é o email de teste de enviar email do Django', 'gdmacedo@gmail.com', ['gdmacedo@hotmail.com'])
            # mensagem  = "Corpo da mensagem principal"
            # email = EmailMessage(subject='Assunto do eMail',
            #                    body='Mensagem Principal',
            #                    from_email=settings.EMAIL_HOST_USER,
            #                    to=['gdmacedo@outlook.com']
            #                    )
            # email.send()

            corpo_email = """
            <p>Você solicitou username para acesso ao nosso ERP.</p>
            <p><b>Username:</b> 
            """
            corpo_email += usuario.username
            corpo_email += """<p>
            <p>Anote e faça login, para ter o melhor.</p>
            """

            msg = email.message.Message()
            msg['Subject'] = "Recuperando seu nome de acesso [Username]"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = get_email
            password = settings.EMAIL_HOST_PASSWORD
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']],
                       msg.as_string().encode('iso-8859-1'))

            request.session.flush()
            # TODO: Utilizar messages do Django
            messages.add_message(
                request, messages.INFO, 'Seu login/Username foi enviado a seu email. Verifica seu email !')
            return redirect('/usuarios/login')

        else:
            messages.add_message(
                request, messages.ERROR, 'O eMail informado, não se encontra em nosso Cadastro!')
            return render(request, 'rcprrusrnme.html')


def fnct_logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')


@login_required(login_url='/usuarios/login/')
def fnct_usrs_prfle(request):
    if request.method == "GET":

        return render(request, 'users_profile.html')

    elif request.method == "POST":
        get_firstname = request.POST.get('firstName')
        get_lastname = request.POST.get('lastName')

        # users = User.objects.filter(username = slct_usernme)
        get_snha = request.POST.get("psswrdsnha")
        get_cnfrmr_snha = request.POST.get('cnfrmar_psswrdsnha')

        get_img_foto = request.FILES.get('foto')

        try:
            if get_img_foto != 'None':

                img_save = Image.open(get_img_foto)
                path = os.path.join(settings.BASE_DIR,
                                    f'media/user_photos/{get_img_foto.name}')
                img_save = img_save.save(path)

                updte_Usario = User.objects.get(id=request.user.id)
                updte_Usario.foto = get_img_foto
                updte_Usario.save()

            else:
                print(get_img_foto)

        except:
            print('Erro em Salvar Foto...')
            print(get_img_foto)

        if get_snha != get_cnfrmr_snha:
            print('Erro ')
            messages.add_message(request, constants.ERROR,
                                 'Confirmação de senha não confere!')
            return redirect('/usuarios/users_profile')

        if len(get_firstname) < 6:
            print('Erro 3')
            messages.add_message(
                request, constants.ERROR, 'Digite um primeiro nome com no mínimo 7 caracters.')
            return redirect('/usuarios/users_profile')

        try:
            updte_Usario = User.objects.get(id=request.user.id)
            updte_Usario.first_name = get_firstname
            updte_Usario.last_name = get_lastname

            updte_Usario.save()

            messages.add_message(
                request, constants.SUCCESS, 'Os Dados Salvo com sucesso...', 'bi bi-check-circle me-1')
            return redirect('/usuarios/users_profile')

        except:
            print('Erro 4')
            messages.add_message(
                request, constants.ERROR, 'Os dados não foram salvo com sucesso...', 'bi bi-exclamation-octagon me-1')
            return redirect('/usuarios/users_profile')


@login_required(login_url='/usuarios/login/')
def fnct_agenda(request):
    if request.method == "GET":
        cAgenda = "Clinica"
        return render(request, 'Agenda.html', {'Slct_Agenda': cAgenda})


@login_required(login_url='/usuarios/login/')
def fnct_My_Profile(request):

    if request.method == "GET":
        slct_id_cliente = request.user

        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)
        slct_Endrs_Cli = Prfl_Endereco.objects.filter(
            cliente=slct_id_cliente.id)

        try:
            slct_id_Perfil, criado = Perfil.objects.get_or_create(
                user=slct_id_cliente,
                defaults={'Foto': 'fotos_perfil/usuario_sem_foto.png'}
            )
            if criado:
                print("Perfil criado!")
        except Exception as e:
            print("Erro ao criar perfil:", e)

        slct_id_Pet_Cli = Pet_Cliente.objects.filter(
            cliente=slct_id_cliente.id)

        return render(request, 'My_Profile.html', {'Endrcs_Cli': slct_Endrs_Cli, 'Pets_Cliente': slct_id_Pet_Cli, 'cliente': slct_id_cliente, 'cGrp_Usuario': Get_cGrp_Usuario(request.user), 'perfil': slct_id_Perfil, 'is_medico': is_medico(request.user)})

    elif request.method == "POST":
        get_firstname = request.POST.get('get_first_nome')
        get_lastname = request.POST.get('get_last_nome')
        get_celula = request.POST.get('get_celular')
        get_cargo = request.POST.get('get_cargo')
        get_descricao = request.POST.get('get_descricao')

        # users = User.objects.filter(username = slct_usernme)
        get_snha = request.POST.get("psswrdsnha")
        get_cnfrmr_snha = request.POST.get('cnfrmar_psswrdsnha')

        get_img_foto = request.FILES.get('foto')

        print(get_img_foto)

        try:
            if get_img_foto is not None:

                img_save = Image.open(get_img_foto)
                path = os.path.join(settings.BASE_DIR,
                                    f'media/fotos_perfil/{get_img_foto.name}')
                img_save = img_save.save(path)

                updte_Usario = User.objects.get(id=request.user.id)
                updte_Perfil, criado = Perfil.objects.get_or_create(
                    user=updte_Usario,
                    defaults={'Foto': 'fotos_perfil/usuario_sem_foto.png'}
                )
                if criado:
                    print("Perfil criado!")

                updte_Perfil.Foto = f'fotos_perfil/{get_img_foto.name}'
                updte_Perfil.save()

                print('Salva Foto no Perfil')
                print(get_img_foto)

                messages.add_message(
                    request, constants.SUCCESS, 'A Foto foi salva com sucesso...', 'bi bi-check-circle me-1')

                return redirect('/usuarios/my-profile/')
            else:
                if get_firstname is None:
                    messages.add_message(
                        request, constants.ERROR, 'A Foto não foi informada...')

                    return redirect('/usuarios/my-profile/')

        except:
            print('Erro em Salvar Foto...')
            print(get_img_foto)

        if get_snha != get_cnfrmr_snha:
            print('Erro ')
            messages.add_message(request, constants.ERROR,
                                 'Confirmação de senha não confere!')
            return redirect('/usuarios/my-profile/')

        if get_firstname is not None:
            if len(get_firstname) < 6:
                print('Erro 3')
                messages.add_message(
                    request, constants.ERROR, 'Digite um primeiro nome com no mínimo 7 caracters.')
                return redirect('/usuarios/my-profile/')

        try:
            updte_Usario = User.objects.get(id=request.user.id)
            updte_Usario.first_name = get_firstname
            updte_Usario.last_name = get_lastname
            updte_Usario.save()

            # updte_Perfil = Perfil.objects.get(user=updte_Usario)

            updte_Perfil, criado = Perfil.objects.get_or_create(
                user=updte_Usario,
                defaults={'Foto': 'fotos_perfil/usuario_sem_foto.png'}
            )
            if criado:
                print("Perfil criado!")

            updte_Perfil.Celular = get_celula
            updte_Perfil.Cargo = get_cargo
            updte_Perfil.Descricao = get_descricao
            updte_Perfil.save()

            messages.add_message(
                request, constants.SUCCESS, 'Os Dados Salvo com sucesso...', 'bi bi-check-circle me-1')
            return redirect('/usuarios/my-profile/')

        except:
            print('Erro 4')
            messages.add_message(
                request, constants.ERROR, 'Os dados não foram salvo com sucesso...', 'bi bi-exclamation-octagon me-1')
            return redirect('/usuarios/my-profile/')


@csrf_exempt  # só para testes! Em produção, use CSRF corretamente
def atualizar_menu_esquerdo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            novo_valor = data.get('id_mn_Esquerdo')

            usuario = Perfil.objects.get(user=request.user.id)  # exemplo fixo
            usuario.id_mn_Esquerdo = novo_valor
            usuario.save()
            print('Status Ok')

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print('erro')
            return JsonResponse({'error': str(e)}, status=444400)

    # Se não for POST, retorna erro
    return JsonResponse({'error': 'Método não permitido'}, status=405)
