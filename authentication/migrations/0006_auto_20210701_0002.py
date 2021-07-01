# Generated by Django 3.2.4 on 2021-07-01 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20210630_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_mentor_approved',
        ),
        migrations.AddField(
            model_name='user',
            name='mentor_status',
            field=models.CharField(choices=[('n/a', 'not applicable'), ('pending', 'pending'), ('approved', 'approved'), ('denied', 'denied')], default='not applicable', max_length=10),
        ),
    ]