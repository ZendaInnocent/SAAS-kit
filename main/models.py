from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Plan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('price', )

    def __str__(self):
        return self.name.title()


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    subscription = models.ForeignKey(
        'Subscription', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    phone = models.CharField('Enter your M-PESA mobile number',
                             max_length=10, help_text='Format: 07xxxxxxxx')
    amount = models.PositiveIntegerField()
    transactionID = models.CharField(max_length=100)
    conversationID = models.CharField(max_length=100,)
    reference_no = models.CharField(max_length=150)

    class Meta:
        ordering = ['-timestamp', ]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    canceled = models.BooleanField(default=False)
    recurrence_period = models.PositiveIntegerField(default=1)
    auto_renewal = models.BooleanField(default=True)
    expires = models.DateField(null=True, default=timezone.now)

    class Meta:
        unique_together = ('user', 'plan', )

    def __str__(self):
        return f'{self.user.name.title()} - {self.plan.name.title()}'


def __user_get_subscription(user):
    return user.subscription_set.first().plan.name


User.add_to_class('get_subscription', __user_get_subscription)
