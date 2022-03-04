# Generated by Django 4.0.3 on 2022-03-04 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphql_project.user')),
            ],
        ),
    ]
