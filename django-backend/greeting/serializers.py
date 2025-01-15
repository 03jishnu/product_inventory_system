
import decimal
from rest_framework import serializers
from .models import Product, Variant, SubVariant

class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['id', 'name', 'option_name', 'total_stock']

    def create(self, validated_data):
        total_stock = decimal.Decimal(validated_data['option_name'].get('stock', 0))
        validated_data['total_stock'] = total_stock

        subvariant = SubVariant.objects.create(**validated_data)
        return subvariant

    def update(self, instance, validated_data):
        instance.option_name = validated_data.get('option_name', instance.option_name)
        instance.total_stock = instance.calculate_total_stock()
        instance.save()

        return instance

class VariantSerializer(serializers.ModelSerializer):
    subvariants = SubVariantSerializer(many=True)

    class Meta:
        model = Variant
        fields = ['id', 'name', 'options', 'subvariants', 'total_stock']

    def create(self, validated_data):
        subvariants_data = validated_data.pop('subvariants', [])
        variant = Variant.objects.create(**validated_data)

        for subvariant_data in subvariants_data:
            SubVariant.objects.create(variant=variant, **subvariant_data)

        variant.total_stock = variant.calculate_total_stock()
        variant.save()

        return variant

    def update(self, instance, validated_data):
        subvariants_data = validated_data.pop('subvariants', [])
        instance.name = validated_data.get('name', instance.name)
        instance.options = validated_data.get('options', instance.options)
        instance.save()

        for subvariant_data in subvariants_data:
            subvariant, created = SubVariant.objects.update_or_create(
                variant=instance, **subvariant_data
            )

        instance.total_stock = instance.calculate_total_stock()
        instance.save()

        return instance

class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'product_id', 'product_code', 'product_name', 'product_image', 'created_date',
                  'updated_date', 'created_user', 'is_favourite', 'active', 'hsn_code', 'total_stock', 'variants']

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        product = Product.objects.create(**validated_data)

        for variant_data in variants_data:
            subvariants_data = variant_data.pop('subvariants', [])
            variant = Variant.objects.create(product=product, **variant_data)
            for subvariant_data in subvariants_data:
                SubVariant.objects.create(variant=variant, **subvariant_data)

            variant.total_stock = variant.calculate_total_stock()
            variant.save()

        product.total_stock = product.calculate_total_stock()
        product.save()

        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', [])
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_image = validated_data.get('product_image', instance.product_image)
        instance.updated_date = validated_data.get('updated_date', instance.updated_date)
        instance.created_user = validated_data.get('created_user', instance.created_user)
        instance.is_favourite = validated_data.get('is_favourite', instance.is_favourite)
        instance.active = validated_data.get('active', instance.active)
        instance.hsn_code = validated_data.get('hsn_code', instance.hsn_code)
        instance.save()

        for variant_data in variants_data:
            subvariants_data = variant_data.pop('subvariants', [])
            variant, created = Variant.objects.update_or_create(
                product=instance, **variant_data
            )
            for subvariant_data in subvariants_data:
                SubVariant.objects.update_or_create(
                    variant=variant, **subvariant_data
                )

            variant.total_stock = variant.calculate_total_stock()
            variant.save()

        instance.total_stock = instance.calculate_total_stock()
        instance.save()

        return instance
