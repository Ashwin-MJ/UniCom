# Generated by Django 2.1.2 on 2019-02-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_feedback_app', '0003_auto_20190213_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='achiev',
            field=models.IntegerField(),
        ),
    ]
