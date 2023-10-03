# Generated by Django 4.1.5 on 2023-10-03 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='accomplishment_image',
            field=models.ImageField(blank=True, null=True, upload_to='certs/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='accomplishments',
            field=models.CharField(default='No accomplishments yet', max_length=100),
        ),
    ]