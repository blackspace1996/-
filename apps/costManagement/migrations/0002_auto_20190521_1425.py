# Generated by Django 2.2.1 on 2019-05-21 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('costManagement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_blockinfo_rawproduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomeinfo',
            name='recorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='记录人'),
        ),
        migrations.AddField(
            model_name='costinfo',
            name='costCompany',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.CompanyInfo', verbose_name='花销公司'),
        ),
        migrations.AddField(
            model_name='costinfo',
            name='recorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='记录人'),
        ),
    ]