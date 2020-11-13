# Generated by Django 3.1.1 on 2020-11-12 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20201107_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(help_text='Format: 255xxxxxxxxx', max_length=12, verbose_name='Enter your M-PESA mobile number')),
                ('amount', models.PositiveIntegerField()),
                ('transactionID', models.CharField(max_length=100)),
                ('conversationID', models.CharField(max_length=100)),
                ('third_convID', models.CharField(max_length=150, verbose_name='ThirdPartyConversationID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
