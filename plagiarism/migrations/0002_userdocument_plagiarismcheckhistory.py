# Generated by Django 5.1 on 2024-08-19 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plagiarism', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('pdf', models.FileField(upload_to='user_documents/')),
                ('content', models.TextField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlagiarismCheckHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity_score', models.FloatField()),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('matched_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plagiarism.document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plagiarism.userdocument')),
            ],
        ),
    ]
