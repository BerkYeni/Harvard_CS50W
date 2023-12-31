# Generated by Django 4.2.5 on 2023-10-22 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_is_closed_auction_sold_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='is_closed',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='sold_to',
        ),
        migrations.AddField(
            model_name='auction',
            name='taken_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sold_auction', to='auctions.bid'),
        ),
    ]
