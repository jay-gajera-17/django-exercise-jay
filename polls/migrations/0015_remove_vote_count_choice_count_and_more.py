# Generated by Django 5.0 on 2024-01-02 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_alter_choice_choice_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='count',
        ),
        migrations.AddField(
            model_name='choice',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=200),
        ),
    ]
