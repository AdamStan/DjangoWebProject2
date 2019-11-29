# Generated by Django 2.1.2 on 2018-10-26 19:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='scheduler',
            name='user',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_scheduler',
            new_name='scheduler',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_student',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_teacher',
            new_name='teacher',
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=None, max_length=32),
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='USER_WITH_NONAME', max_length=64, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='whenCreated',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Professor',
        ),
        migrations.DeleteModel(
            name='Scheduler',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
