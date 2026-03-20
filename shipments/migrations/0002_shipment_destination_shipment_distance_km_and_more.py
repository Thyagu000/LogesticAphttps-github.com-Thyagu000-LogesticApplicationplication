

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='destination',
            field=models.CharField(default='Unknown', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='distance_km',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='pickup_location',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipment',
            name='rate_per_km',
            field=models.FloatField(default=5),
        ),
        migrations.AddField(
            model_name='shipment',
            name='total_charge',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
