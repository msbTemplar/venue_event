# Generated by Django 5.0.4 on 2024-05-12 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_manager_alter_venue_email_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='owner',
            field=models.IntegerField(default=1, verbose_name='Venue Owner'),
        ),
    ]
