# Generated by Django 2.1.4 on 2018-12-13 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_you_are_following', to='following.CustomUser')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_following_you', to='following.CustomUser')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='blocked_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='following.CustomUser'),
        ),
        migrations.AddField(
            model_name='block',
            name='blocker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_you_are_blocking', to='following.CustomUser'),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'following')},
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together={('blocker', 'blocked_user')},
        ),
    ]
