# Generated by Django 4.1.3 on 2022-11-24 04:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('repayment_api', '0005_alter_loan_loan_amount_alter_loan_loan_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repaymentschedule',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
