# Generated by Django 4.0 on 2022-01-10 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_seller_pic_alter_seller_addressline1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('addressline1', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('addressline2', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('addressline3', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('pin', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
            ],
        ),
        migrations.RenameField(
            model_name='seller',
            old_name='emial',
            new_name='email',
        ),
        migrations.RemoveField(
            model_name='product',
            name='specification',
        ),
        migrations.AddField(
            model_name='product',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]