# Generated by Django 3.1.5 on 2021-01-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20210128_0841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mypost',
            name='post_category',
        ),
        migrations.AddField(
            model_name='mypost',
            name='post_category',
            field=models.ManyToManyField(to='myblog.PostCategory', verbose_name='文章分类'),
        ),
    ]
