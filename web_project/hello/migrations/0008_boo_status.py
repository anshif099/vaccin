# Generated by Django 5.1.4 on 2025-01-02 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_boo_delete_vcbk'),
    ]

    operations = [
        migrations.AddField(
            model_name='boo',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]
