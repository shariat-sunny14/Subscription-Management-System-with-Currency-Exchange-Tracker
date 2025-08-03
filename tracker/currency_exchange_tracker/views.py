import requests
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Subscription, Plan, ExchangeRateLog
from .serializers import SubscriptionSerializer, ExchangeRateLogSerializer
from datetime import timedelta, date
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.db.models.functions import TruncDate
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request):
    plan_id = request.data.get('plan_id')
    try:
        plan = Plan.objects.get(id=plan_id)
        end_date = date.today() + timedelta(days=plan.duration_days)

        with transaction.atomic():
            Subscription.objects.create(user=request.user, plan=plan, end_date=end_date)
        return Response({'message': 'Subscription created.'})
    except Plan.DoesNotExist:
        return Response({'error': 'Invalid plan ID'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_subscriptions(request):
    subs = Subscription.objects.filter(user=request.user)
    return Response(SubscriptionSerializer(subs, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    sub_id = request.data.get('subscription_id')
    try:
        sub = Subscription.objects.get(id=sub_id, user=request.user)
        sub.status = 'cancelled'
        sub.save()
        return Response({'message': 'Subscription cancelled.'})
    except Subscription.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['GET'])
def exchange_rate(request):
    base = request.GET.get('base', 'USD')
    target = request.GET.get('target', 'BDT')
    url = f"https://v6.exchangerate-api.com/v6/b59c4a17b2a3bab1758ce430/latest/{base}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data['conversion_rates'][target]
        ExchangeRateLog.objects.create(base_currency=base, target_currency=target, rate=rate, ss_creator=request.user)
        return Response({'base': base, 'target': target, 'rate': rate})
    return Response({'error': 'Failed to fetch rate'}, status=500)

@login_required
def exchange_rate_view(request):
    base = request.GET.get('base', 'USD')
    target = request.GET.get('target', 'BDT')
    url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/{base}"

    rate = None
    error = None

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if target in data['conversion_rates']:
                rate = data['conversion_rates'][target]
                ExchangeRateLog.objects.create(
                    base_currency=base,
                    target_currency=target,
                    rate=rate,
                    ss_creator=request.user,
                )
            else:
                error = "Invalid target currency."
        else:
            error = "Failed to fetch exchange rate."
    except requests.RequestException:
        error = "External API request failed."

    context = {
        'base': base,
        'target': target,
        'rate': rate,
        'error': error,
    }
    return render(request, 'exchange_tracker.html', context)


@login_required
def subscribe_view(request):
    plans = Plan.objects.all()
    today = now().date()

    # Filter out 'expired' from status choices
    status_choices = [choice for choice in Subscription.STATUS_CHOICES if choice[0] != 'expired']

    # Get user_id from POST or fallback to request.user.id if not POST
    user_id = None
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
    else:
        user_id = request.user.id if request.user.is_authenticated else None

    # Fetch user instance
    try:
        user_obj = User.objects.get(id=user_id)
    except (User.DoesNotExist, TypeError):
        user_obj = None

    # Get latest subscription for that user
    latest_sub = None
    if user_obj:
        latest_sub = Subscription.objects.filter(user=user_obj).order_by('-end_date').first()

    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        status = request.POST.get('status', 'active')

        # Validate inputs
        if not user_obj:
            return render(request, 'subscribe_form.html', {
                'plans': plans,
                'status_choices': status_choices,
                'error': 'Invalid user.',
                'latest_sub': latest_sub,
            })

        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return render(request, 'subscribe_form.html', {
                'plans': plans,
                'status_choices': status_choices,
                'error': 'Invalid plan selected!',
                'latest_sub': latest_sub,
            })

        with transaction.atomic():
            end_date = today + timedelta(days=plan.duration_days)

            if latest_sub:
                # Update existing subscription
                latest_sub.plan = plan
                latest_sub.end_date = end_date
                latest_sub.status = status
                latest_sub.save()
                msg = f'Subscription updated to {plan.name} for user {user_obj.username}.'
            else:
                # Create new subscription
                Subscription.objects.create(
                    user=user_obj,
                    plan=plan,
                    end_date=end_date,
                    status=status
                )
                msg = f'Subscribed {user_obj.username} to {plan.name} successfully!'

        # Refresh latest_sub after update/create
        latest_sub = Subscription.objects.filter(user=user_obj).order_by('-end_date').first()

        return render(request, 'subscribe_form.html', {
            'plans': plans,
            'latest_sub': latest_sub,
            'status_choices': status_choices,
            'success': msg,
            'user': user_obj,
        })

    # GET request
    return render(request, 'subscribe_form.html', {
        'plans': plans,
        'latest_sub': latest_sub,
        'status_choices': status_choices,
        'user': user_obj,
    })

@login_required
def cancel_subscription_view(request):
    try:
        subscription = Subscription.objects.get(user=request.user, status='active')
    except Subscription.DoesNotExist:
        subscription = None

    if request.method == 'POST' and subscription:
        subscription.status = 'cancelled'
        subscription.save()
        # return render(request, 'cancel_subscription.html', {
        #     'success': 'Your subscription has been cancelled.',
        #     'subscription': subscription
        # })
        return redirect('currency_exchange:subscribe')

    return render(request, 'cancel_subscription.html', {
        'subscription': subscription
    })
    
    
@login_required
def exchange_rate_history_api(request):
    base = request.GET.get('base')
    target = request.GET.get('target')

    end_date = now().date()
    start_date = end_date - timedelta(days=6)

    queryset = ExchangeRateLog.objects.filter(
        base_currency=base,
        target_currency=target,
        fetched_at__date__range=(start_date, end_date)
    ).order_by('fetched_at')

    data = [
        {
            "datetime": log.fetched_at.strftime("%Y-%m-%d %H:%M:%S"),
            "rate": float(log.rate)
        }
        for log in queryset
    ]

    return JsonResponse(data, safe=False)

@login_required
def subscription_list_view(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    return render(request, 'subscriptions_list.html', {
        'subscriptions': subscriptions
    })

@login_required
def exchange_rate_list_view(request):
    exchange_rates = ExchangeRateLog.objects.all().order_by('-fetched_at')
    return render(request, 'exchange_rate_logs.html', {
        'exchange_rates': exchange_rates
    })