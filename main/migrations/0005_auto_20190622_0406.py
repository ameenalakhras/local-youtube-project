# Generated by Django 2.2.1 on 2019-06-22 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190622_0347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='audio',
            name='image_file',
            field=models.ImageField(null=True, upload_to='home/amin/Desktop/Desktop /youtube project/jjj/staticfiles/media/images/'),
        ),
        migrations.AddField(
            model_name='audio',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
