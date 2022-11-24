# Generated by Django 4.1.3 on 2022-11-24 04:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repayment_api', '0003_repaymentschedules'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepaymentSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_no', models.PositiveIntegerField()),
                ('payment_amount', models.DecimalField(decimal_places=6, max_digits=21)),
                ('principal', models.DecimalField(decimal_places=6, max_digits=21)),
                ('interest', models.DecimalField(decimal_places=6, max_digits=21)),
                ('balance', models.DecimalField(decimal_places=6, max_digits=21)),
                ('created_at', models.DateField(default=datetime.date(2022, 11, 24))),
                ('updated_at', models.DateField(default=datetime.date(2022, 11, 24))),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='loan',
            name='updated_at',
            field=models.DateField(default=datetime.date(2022, 11, 24)),
        ),
        migrations.DeleteModel(
            name='RepaymentSchedules',
        ),
        migrations.AddField(
            model_name='repaymentschedule',
            name='loan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repayment_api.loan'),
        ),
    ]