from rest_framework import serializers
from .models import Subscription, Plan, ExchangeRateLog

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'

class ExchangeRateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = '__all__'
