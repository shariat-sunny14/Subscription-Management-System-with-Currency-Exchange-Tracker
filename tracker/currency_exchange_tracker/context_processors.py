
from currency_exchange_tracker.models import Subscription


def active_subscription(request):
    if request.user.is_authenticated:
        try:
            sub = Subscription.objects.filter(user=request.user).order_by('-end_date').first()
        except Subscription.DoesNotExist:
            sub = None
        return {'active_subscription': sub}
    return {'active_subscription': None}