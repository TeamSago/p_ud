# Generated by Django 4.0 on 2022-05-12 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('contents', models.TextField(verbose_name='contents')),
                ('write_dttm', models.DateTimeField(auto_now_add=True, verbose_name='upload Date')),
                ('board_name', models.CharField(default='Python', max_length=32, verbose_name='board category')),
                ('update_dttm', models.DateTimeField(auto_now=True, verbose_name='lastest updated')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='hits')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='writer')),
            ],
            options={
                'verbose_name': 'board',
                'verbose_name_plural': 'board',
                'db_table': 'board',
            },
        ),
    ]
