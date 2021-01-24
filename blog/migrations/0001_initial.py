# Generated by Django 3.1.5 on 2021-01-24 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('content', models.TextField()),
                ('created_time', models.DateField(auto_now_add=True)),
                ('c_parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
            ],
        ),
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=20)),
                ('post_tag', models.CharField(max_length=20)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('updated_time', models.DateField(auto_now=True)),
                ('post_view', models.IntegerField(default=0)),
                ('content_path', models.CharField(max_length=100)),
                ('comments', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
            ],
        ),
    ]