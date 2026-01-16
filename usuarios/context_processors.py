'''
Para tornar o Perfil do usuário logado acessível em qualquer template HTML do Django 
sem precisar defini-lo manualmente em cada view, você pode usar um context processor. 

Isso é uma forma elegante e centralizada de injetar dados em todos os templates renderizados.
'''
from usuarios.models import Perfil, UfEstados




def perfil_usuario(request):
    if request.user.is_authenticated:
        # Seleciona o Perfil do Usuário logado.
        prfl_Slct, _ = Perfil.objects.get_or_create(
            user=request.user,
            defaults={'Foto': 'user_photos/usuario_sem_foto.png'}
        )
        return {'Perfil_User': prfl_Slct}
    return {}


def uf_estados(request):
    GEt_UFEstados = UfEstados.objects.all().order_by('UfEstados')
    return {'UFEstdos_All': GEt_UFEstados}

