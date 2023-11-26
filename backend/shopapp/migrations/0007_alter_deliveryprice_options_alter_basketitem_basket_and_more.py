# Generated by Django 4.2.5 on 2023-11-26 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_deliveryprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliveryprice',
            options={'verbose_name': 'Стоимость доставки'},
        ),
        migrations.AlterField(
            model_name='basketitem',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to='shopapp.basket'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('validity_period', models.CharField(max_length=20)),
                ('success', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pay_order', to='shopapp.order')),
            ],
        ),
    ]
