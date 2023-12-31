# Generated by Django 4.2.1 on 2023-06-07 20:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0, verbose_name='User votes for the step'),
        ),
        migrations.AlterField(
            model_name='step',
            name='level',
            field=models.IntegerField(default=0, verbose_name='Level of the user'),
        ),
        migrations.AlterField(
            model_name='step',
            name='step_description',
            field=models.CharField(max_length=1000, verbose_name='Method description'),
        ),
        migrations.AlterField(
            model_name='step',
            name='step_title',
            field=models.CharField(max_length=200, verbose_name='Method title'),
        ),
    ]
