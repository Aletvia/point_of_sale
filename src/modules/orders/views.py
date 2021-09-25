from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict

from .models import Order
from .serializers import SerializedOrder
from modules.inventory.models import Products


class OrdersView(APIView):
    """
        View dedicated to:
            - List all existing orders
            - Create a new order
            - Retrieve an existing order
    """

    def get(self, request, id=None):
        if id:
            order = Order.objects.get(id=id)
            print(
                "////////////////////////////////GET RETRIEVE A ORDER////////////////////////////////")
            return Response(model_to_dict(order), status=200)
        else:
            orders = Order.objects.all()
            serialized_orders = SerializedOrder(orders, many=True)
            print(
                "////////////////////////////////GET LIST ORDERS////////////////////////////////")
            return Response(serialized_orders.data, status=200)

    def post(self, request):
        print(
            "////////////////////////////////CREANDO  ORDEN////////////////////////////////")
        try:
            d = request.data
            order = create_order(d)
            total = order['total']
            items = order['items']
            if total > 0:
                order_s = Order(
                    items=items,
                    total=total
                )
                order_s.save()
                return Response({
                                'id': order_s.id,
                                'items': order_s.items,
                                'total': order_s.total
                                },
                                status=201)
        except Exception as e:
            return Response({"Status": "BAD", "End": e}, status=405)


def create_order(data):
    try:
        items_init = data['items']
        total = 0
        order = {
            'items': [],
            'total': 0
        }
        for prod in items_init:
            item = {}
            quantity = float(prod["quantity"])
            product = Products.objects.get(id=prod["id"])
            if product.stock >= quantity:
                unit_price = float(product.unit_price)
                total_item = quantity * unit_price
                total = total + total_item
                item = {
                    'description': product.description,
                    'quantity': prod["quantity"],
                    'unit_price': unit_price,
                    'total': total_item
                }
                order["items"].append(item)
                product.stock = product.stock - quantity
                product.save()
            order['total'] = round(total, 2)
        return order
    except Exception as error:
        return {
            'items': [],
            'total': 0,
            'error': error
        }
