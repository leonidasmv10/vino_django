from .models import Perfil


from .models import Perfil


def user_profile(request):
    if request.user.is_authenticated:
        perfil = Perfil.objects.filter(user=request.user).first()
        return {
            "monedas": perfil.monedas if perfil else 0,
            "username": perfil.user.username if perfil else "username",
        }
    return {
        "monedas": 0,
        "username": "username",
    }
