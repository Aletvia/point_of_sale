from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Products
from .serializers import SerializedProducts

class ProductsView(APIView):
    """
        View dedicated to:
            - List all existing products
            - Create a new product
            - Retrieve an existing product
            - Update an existing product
    """
    
    def get( self, request, id=None ):
        if id:
            product = Products.objects.get( id = id )
            serialized_product = SerializedProducts( product, many = False )
            print ( "////////////////////////////////GET RETRIEVE A PRODUCT////////////////////////////////" )
            return JsonResponse( serialized_product.data, status = 200 )
        else:
            products = Products.objects.all()
            serialized_products = SerializedProducts( products, many = True )
            print ( "////////////////////////////////GET LIST PRODUCTS////////////////////////////////" )
            return JsonResponse( serialized_products.data, safe = False, status = 200 )

    def post( self, request ):
        try:
            serialized_product = SerializedProducts( data = request.data )
            if serialized_product.is_valid():
                description = serialized_product.validated_data.get('description')
                unit_price = serialized_product.validated_data.get('unit_price')
                stock = serialized_product.validated_data.get('stock')
                product = Products( 
                                    description = description, 
                                    unit_price = unit_price, 
                                    stock = stock 
                                )
                product.save()
                return JsonResponse({'description':description,'unit_price':unit_price,'stock':stock}, status=201)
                print ( "////////////////////////////////POST CREATE A PRODUCT////////////////////////////////" )
        except Exception as e:
            return JsonResponse(serialized_product.errors, status=400)

    def put( self, request, id ):
        try:
            product = Products.objects.get( id = id )
            serialized_product = SerializedProducts( product, request.data )
            if serialized_product.is_valid():
                print ( "////////////////////////////////PUT UPDATE A PRODUCT////////////////////////////////" )
                serialized_product.save()
                return JsonResponse( serialized_product.data, status = 200 )
        except Exception as e:
            return JsonResponse( serialized_product.errors, status = 405 )

    def patch( self, request, id ):
        try:
            product = Products.objects.get( id = id )
            serialized_product = SerializedProducts( product, data = request.data, partial = True )
            if serialized_product.is_valid():
                serialized_product.save()
                print ( "////////////////////////////////PATCH ACTUALIZANDO  PRODUCTO////////////////////////////////" )
                return JsonResponse( serialized_product.data, status = 200 )
        except Exception as e:
            return JsonResponse( serialized_product.errors, status = 405 )