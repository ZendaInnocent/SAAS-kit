from django.contrib import admin

from .models import Plan, Subscription, Transaction


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan', 'user', 'active', 'canceled', 'expires', )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
