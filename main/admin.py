from django.contrib import admin

from .models import Payment, Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan', 'user', 'active', 'canceled', 'expires', )


@admin.register(Payment)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'amount', )
    readonly_fields = ('user',  'phone', 'amount',
                       'transactionID', 'conversationID', 'third_convID', )
