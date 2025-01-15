# Generated by Django 5.0.6 on 2025-01-12 17:29

import django.db.models.deletion
import uuid
import versatileimagefield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_id', models.BigIntegerField(unique=True)),
                ('product_code', models.CharField(max_length=255, unique=True)),
                ('product_name', models.CharField(max_length=255)),
                ('product_image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='uploads/')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('is_favourite', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('hsn_code', models.CharField(blank=True, max_length=255, null=True)),
                ('total_stock', models.DecimalField(blank=True, decimal_places=8, default=0.0, max_digits=20, null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'products_product',
                'ordering': ('-created_date', 'product_id'),
                'unique_together': {('product_code', 'product_id')},
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('options', models.JSONField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='greeting.product')),
            ],
        ),
        migrations.CreateModel(
            name='SubVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('option_name', models.JSONField()),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subvariants', to='greeting.variant')),
            ],
        ),
    ]
