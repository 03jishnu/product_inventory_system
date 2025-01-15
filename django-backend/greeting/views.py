from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Variant, SubVariant
from .serializers import ProductSerializer, VariantSerializer, SubVariantSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from uuid import UUID
from django.apps import apps
from decimal import Decimal
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_products(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    products = Product.objects.prefetch_related('variants__subvariants').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)






    
    


@api_view(['GET'])
def get_product_detail(request, product_id):
    print(f"Product ID received from URL: {product_id}") 

   
    try:
        
        product_id = str(UUID(product_id))  
    except ValueError:
        return JsonResponse({'error': 'Invalid product ID format'}, status=400)

    try:
       
        product = Product.objects.prefetch_related('variants__subvariants').get(id=product_id)

        
        product_data = {
            'id': product.id,
            'product_name': product.product_name,
            'product_code': product.product_code,
            'total_stock': product.total_stock,
            'variants': [
                {
                    'id': variant.id,
                    'name': variant.name,
                    'options': variant.options if hasattr(variant, 'options') else [],
                    'subvariants': [
                        {
                            'id': subvariant.id,
                            'name': subvariant.name,
                            'option_name': subvariant.option_name,
                            
                        }
                        for subvariant in variant.subvariants.all()
                    ]
                }
                for variant in product.variants.all()
            ]
        }

        return JsonResponse(product_data)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    except Exception as e:
      
        print(f"Unexpected error: {e}") 
        return JsonResponse({'error': 'Internal server error', 'details': str(e)}, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def create_product(request):
    print("Received data:", request.data)  

   
    data = request.data.copy()
    data['created_user'] = request.user.id  
   
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_stock(request, product_id, variant_id=None, subvariant_id=None):
    option_name = request.data.get('option_name')  
    stock_to_add = request.data.get('stock', 0)   

    
    try:
        stock_to_add = int(stock_to_add)
    except (ValueError, TypeError):
        return Response({"detail": "Invalid stock value."}, status=status.HTTP_400_BAD_REQUEST)

    def update_product_stock(product_id):
        product = Product.objects.get(id=product_id)
        product.total_stock = product.calculate_total_stock()
        product.save()

    if variant_id:
        try:
            variant = Variant.objects.get(id=variant_id, product_id=product_id)
            options = variant.options  
            
           
            for option in options:
                if option.get('option_name') == option_name:
                    current_stock = int(option.get('stock', 0))  
                    option['stock'] = current_stock + stock_to_add  
                    variant.total_stock += stock_to_add 
                    variant.save()
                    break
            else:
                return Response({"detail": f"Option '{option_name}' not found in variant."}, status=status.HTTP_404_NOT_FOUND)

           
            update_product_stock(product_id)

            return Response({'message': 'Variant stock updated successfully', 'options': variant.options}, status=status.HTTP_200_OK)
        
        except Variant.DoesNotExist:
            return Response({"detail": "Variant not found."}, status=status.HTTP_404_NOT_FOUND)

   
    if subvariant_id:
        SubVariant = apps.get_model('greeting', 'SubVariant')
        try:
           
            subvariant = SubVariant.objects.get(id=subvariant_id, variant__product_id=product_id)
            option_name_dict = subvariant.option_name  
           
            if isinstance(option_name_dict, dict):
                if option_name_dict.get('option_name') == option_name:
                    current_stock = int(option_name_dict.get('stock', 0))  
                    option_name_dict['stock'] = current_stock + stock_to_add  
                    subvariant.total_stock += stock_to_add 
                    subvariant.option_name = option_name_dict  
                    subvariant.save()

                    update_product_stock(product_id)

                    return Response({'message': 'Subvariant stock updated successfully', 'options': subvariant.option_name}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": f"Option '{option_name}' not found in subvariant."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Invalid option_name structure in subvariant."}, status=status.HTTP_400_BAD_REQUEST)

        except SubVariant.DoesNotExist:
            return Response({"detail": "Subvariant not found."}, status=status.HTTP_404_NOT_FOUND)

    
    return Response({"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)









@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_stock(request, product_id, variant_id=None, subvariant_id=None):
    option_name = request.data.get('option_name')  
    stock_to_remove = request.data.get('stock', 0)   

   
    try:
        stock_to_remove = int(stock_to_remove)
    except (ValueError, TypeError):
        return Response({"detail": "Invalid stock value."}, status=status.HTTP_400_BAD_REQUEST)

    
    def update_product_stock(product_id):
        product = Product.objects.get(id=product_id)
        product.total_stock = product.calculate_total_stock()
        product.save()

   
    if variant_id:
        try:
            variant = Variant.objects.get(id=variant_id, product_id=product_id)
            options = variant.options 
            for option in options:
                if option.get('option_name') == option_name:
                    current_stock = int(option.get('stock', 0)) 
                    if current_stock < stock_to_remove:
                        return Response({"detail": "Insufficient stock to remove."}, status=status.HTTP_400_BAD_REQUEST)
                    option['stock'] = current_stock - stock_to_remove 
                    variant.total_stock -= stock_to_remove  
                    variant.save()
                    break
            else:
                return Response({"detail": f"Option '{option_name}' not found in variant."}, status=status.HTTP_404_NOT_FOUND)

            update_product_stock(product_id)

            return Response({'message': 'Variant stock removed successfully', 'options': variant.options}, status=status.HTTP_200_OK)
        
        except Variant.DoesNotExist:
            return Response({"detail": "Variant not found."}, status=status.HTTP_404_NOT_FOUND)

    if subvariant_id:
        SubVariant = apps.get_model('greeting', 'SubVariant')
        try:
            subvariant = SubVariant.objects.get(id=subvariant_id, variant__product_id=product_id)
            option_name_dict = subvariant.option_name  

            if isinstance(option_name_dict, dict):
                if option_name_dict.get('option_name') == option_name:
                    current_stock = int(option_name_dict.get('stock', 0))  
                    if current_stock < stock_to_remove:
                        return Response({"detail": "Insufficient stock to remove."}, status=status.HTTP_400_BAD_REQUEST)
                    option_name_dict['stock'] = current_stock - stock_to_remove  
                    subvariant.total_stock -= stock_to_remove  
                    subvariant.option_name = option_name_dict  
                    subvariant.save()

                    update_product_stock(product_id)

                    return Response({'message': 'Subvariant stock removed successfully', 'options': subvariant.option_name}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": f"Option '{option_name}' not found in subvariant."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Invalid option_name structure in subvariant."}, status=status.HTTP_400_BAD_REQUEST)

        except SubVariant.DoesNotExist:
            return Response({"detail": "Subvariant not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
