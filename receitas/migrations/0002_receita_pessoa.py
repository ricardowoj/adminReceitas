# Generated by Django 3.0.7 on 2020-06-21 14:53

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='pessoa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
