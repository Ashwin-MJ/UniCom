# Generated by Django 2.1.2 on 2019-02-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_feedback_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='colour',
            field=models.CharField(default='#009999', max_length=7),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='Empty', max_length=30),
        ),
    ]
