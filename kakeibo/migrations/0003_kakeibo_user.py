# Generated by Django 3.1.5 on 2021-01-21 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kakeibo', '0002_auto_20210117_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='kakeibo',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='auth.user', verbose_name='ユーザー'),
            preserve_default=False,
        ),
    ]
