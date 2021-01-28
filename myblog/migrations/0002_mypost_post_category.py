# Generated by Django 3.1.5 on 2021-01-28 08:39

from django.db import migrations, models
import django.db.models.deletion
import myblog.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='post_category',
            field=models.ForeignKey(default=myblog.models.default_category, on_delete=django.db.models.deletion.SET_DEFAULT, to='myblog.postcategory', verbose_name='文章分类'),
        ),
    ]
