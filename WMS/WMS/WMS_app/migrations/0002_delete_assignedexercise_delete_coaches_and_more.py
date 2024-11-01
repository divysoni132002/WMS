# Generated by Django 5.1.2 on 2024-10-29 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WMS_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AssignedExercise',
        ),
        migrations.DeleteModel(
            name='Coaches',
        ),
        migrations.RemoveField(
            model_name='fitnessplan',
            name='exercise',
        ),
        migrations.DeleteModel(
            name='fitness_info',
        ),
        migrations.RemoveField(
            model_name='fitnessplan',
            name='submission',
        ),
        migrations.DeleteModel(
            name='LQ_data',
        ),
        migrations.DeleteModel(
            name='MenstrualCyclePrediction',
        ),
        migrations.DeleteModel(
            name='OccStress',
        ),
        migrations.DeleteModel(
            name='PostPlanData',
        ),
        migrations.DeleteModel(
            name='PSSResponse',
        ),
        migrations.DeleteModel(
            name='SleepScore',
        ),
        migrations.DeleteModel(
            name='Exercise',
        ),
        migrations.DeleteModel(
            name='FitnessPlan',
        ),
        migrations.DeleteModel(
            name='FitnessPlanSubmission',
        ),
    ]
