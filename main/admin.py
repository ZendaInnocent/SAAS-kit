from django.contrib import admin

from .models import Plan, Subscription, Transaction


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
