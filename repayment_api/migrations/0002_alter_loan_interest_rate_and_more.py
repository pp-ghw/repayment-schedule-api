# Generated by Django 4.1.3 on 2022-11-28 05:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repayment_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="interest_rate",
            field=models.DecimalField(
                decimal_places=6,
                max_digits=21,
                validators=[
                    django.core.validators.MaxValueValidator(50),
                    django.core.validators.MinValueValidator(1),
                ],
            ),
        ),
        migrations.AlterModelTable(
            name="repaymentschedule",
            table="repayment_schedule",
        ),
    ]
