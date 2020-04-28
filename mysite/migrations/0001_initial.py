# Generated by Django 3.0.5 on 2020-04-28 12:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='username')),
                ('Phone_Number', models.CharField(default='', max_length=14)),
                ('Date', models.DateField(default=datetime.datetime(2020, 4, 28, 12, 57, 19, 731922, tzinfo=utc))),
                ('Profile_Picture', models.ImageField(default='default.png', upload_to='user_pics')),
                ('Status', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='', max_length=50)),
                ('Date', models.DateField(default=datetime.datetime(2020, 4, 28, 12, 57, 19, 731922, tzinfo=utc))),
                ('Post', models.TextField(default='', max_length=500)),
                ('Likes', models.IntegerField(default=0)),
                ('Remark', models.CharField(default='', max_length=50)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment', models.TextField(default='', max_length=100)),
                ('Date', models.DateField(default=datetime.datetime(2020, 4, 28, 12, 57, 19, 731922, tzinfo=utc))),
                ('Likes', models.IntegerField(default=0)),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Posts')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
