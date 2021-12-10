from baskets.models import Basket


def baskets(request):
    print('context processor basket works')
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = Basket.objects.filter(user=request.user).select_related()
    return {'baskets': baskets_list}