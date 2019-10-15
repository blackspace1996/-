# Generated by Django 2.2.1 on 2019-05-21 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HarvestInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harvestTime', models.DateField(auto_now_add=True, verbose_name='收获时间')),
                ('harvestTips', models.CharField(max_length=999, null=True, verbose_name='收获备注')),
                ('hashWords', models.CharField(max_length=256, verbose_name='记录hash')),
                ('isNormal', models.BooleanField(default='True', verbose_name='是否正常')),
                ('isStore', models.BooleanField(default='False', verbose_name='是否入库')),
            ],
            options={
                'verbose_name': '确认信息',
                'verbose_name_plural': '确认信息',
            },
        ),
        migrations.CreateModel(
            name='MeasureConfirmingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isConfirming', models.BooleanField(default=False, verbose_name='是否确认')),
                ('confirmingTips', models.CharField(default='', max_length=999, verbose_name='确认备注')),
                ('confirmingTime', models.DateField(null=True, verbose_name='确认时间')),
                ('confirmingMember', models.CharField(default='', max_length=20, verbose_name='确认人')),
                ('hashWords', models.CharField(default='', max_length=256, verbose_name='记录hash')),
                ('isNormal', models.BooleanField(default='True', verbose_name='是否正常')),
            ],
            options={
                'verbose_name': '播种信息',
                'verbose_name_plural': '播种信息',
            },
        ),
        migrations.CreateModel(
            name='SowInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sowingName', models.CharField(max_length=20, verbose_name='名称')),
                ('sowingTime', models.DateField(auto_now_add=True, verbose_name='播种时间')),
                ('sowingTips', models.CharField(max_length=999, verbose_name='播种备注')),
                ('hashWords', models.CharField(max_length=256, verbose_name='记录hash')),
                ('isNormal', models.BooleanField(default='True', verbose_name='是否正常')),
                ('isHarvest', models.BooleanField(default='False', verbose_name='是否收获')),
            ],
            options={
                'verbose_name': '播种信息',
                'verbose_name_plural': '播种信息',
            },
        ),
    ]