# Generated by Django 5.1.5 on 2025-01-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='faculty_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='Unknown', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='student_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student', max_length=10),
        ),
    ]
