# Generated by Django 2.1.2 on 2018-11-24 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0017_scheduledsubject_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledsubject',
            name='teacher',
            field=models.ForeignKey(default=None, null=True, on_delete=True, to='entities.Teacher'),
        ),
    ]
