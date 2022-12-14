# Generated by Django 4.1.3 on 2022-11-28 03:26

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import repayment_api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "loan_amount",
                    models.DecimalField(
                        decimal_places=6,
                        max_digits=21,
                        validators=[
                            django.core.validators.MaxValueValidator(100000000),
                            django.core.validators.MinValueValidator(1000),
                        ],
                    ),
                ),
                (
                    "loan_term",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(50),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
                (
                    "interest_rate",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        validators=[
                            django.core.validators.MaxValueValidator(50),
                            django.core.validators.MinValueValidator(1),
                        ],
                    ),
                ),
                (
                    "loan_month",
                    models.IntegerField(
                        validators=[repayment_api.models.Loan.validate_month]
                    ),
                ),
                (
                    "loan_year",
                    models.IntegerField(
                        validators=[repayment_api.models.Loan.validate_year]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "loan",
            },
        ),
        migrations.CreateModel(
            name="RepaymentSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_no", models.PositiveIntegerField()),
                (
                    "payment_amount",
                    models.DecimalField(decimal_places=6, max_digits=21),
                ),
                ("principal", models.DecimalField(decimal_places=6, max_digits=21)),
                ("interest", models.DecimalField(decimal_places=6, max_digits=21)),
                ("balance", models.DecimalField(decimal_places=6, max_digits=21)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateTimeField()),
                (
                    "loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repayment_api.loan",
                    ),
                ),
            ],
            options={
                "db_table": "repaymentschedule",
            },
        ),
    ]
