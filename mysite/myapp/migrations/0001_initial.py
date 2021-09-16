# Generated by Django 3.2.7 on 2021-09-15 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MachineInfo',
            fields=[
                ('id', models.AutoField(db_column='ID', default=-1, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('serialNum', models.CharField(max_length=50)),
                ('swVersion', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'MachineInfo',
            },
        ),
        migrations.CreateModel(
            name='MachineStatus',
            fields=[
                ('id', models.AutoField(db_column='ID', default=-1, primary_key=True, serialize=False)),
                ('Status', models.CharField(max_length=50)),
                ('startTime', models.CharField(default='01-01-1900 00:00:00', max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=255)),
                ('machineID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.machineinfo')),
                ('startUserID', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MachineStatus',
            },
        ),
    ]
