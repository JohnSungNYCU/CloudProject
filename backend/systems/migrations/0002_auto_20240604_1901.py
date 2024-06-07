# Generated by Django 3.0.3 on 2024-06-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='group',
            name='memo',
            field=models.TextField(blank=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='group',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='memo',
            field=models.TextField(blank=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='memo',
            field=models.TextField(blank=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='role',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='memo',
            field=models.TextField(blank=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]