# Generated by Django 4.0.1 on 2022-02-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myexpense', '0002_alter_exptransactions_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackmoney',
            name='p_name',
            field=models.CharField(max_length=50, verbose_name='Person Name'),
        ),
        migrations.AlterField(
            model_name='trackmoney',
            name='p_number',
            field=models.CharField(max_length=10, verbose_name='Mobile Number'),
        ),
    ]
