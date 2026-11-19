
from django.http import JsonResponse


def ping(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Доступ запрещён. Требуется авторизация.'
        }, status=403)

    return JsonResponse({
        'status': 'ok',
        'service': 'EcoPoints API'
    })
