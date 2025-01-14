# Generated by Django 5.1.4 on 2025-01-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('소설', '소설'), ('시/에세이', '시/에세이'), ('인문', '인문'), ('기타', '기타'), ('자기계발', '자기계발')], default='기타', max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=20)),
                ('publisher', models.CharField(max_length=20)),
                ('image', models.CharField(blank=True, max_length=300)),
                ('point', models.CharField(blank=True, max_length=100)),
                ('story', models.TextField(blank=True)),
                ('prompt', models.TextField(blank=True)),
                ('book_url', models.URLField(blank=True, max_length=1000)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
