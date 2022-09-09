from django.shortcuts import render,get_object_or_404
from .models import Order
from rest_framework import generics,status
from . import serializers
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

User=get_user_model()

class OrderCreateListView(generics.GenericAPIView):
    serializer_class=serializers.OrderSerializer
    queryset=Order.objects.all()
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Get all Orders")
    def get(self,request):
        orders=Order.objects.all()
        serialiser=self.serializer_class(instance=orders,many=True)
        return Response(data=serialiser.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_summary="Create an order")
    def post(self,request):
        data=request.data
        
        user=request.user
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderDetailListView(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailSerializer
    @swagger_auto_schema(operation_summary="View the detail of an order by its ID")
    def get(self,request,order_id):
        order=get_object_or_404(Order,pk=order_id)
        serialiser=self.serializer_class(instance=order)
        return Response(data=serialiser.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_summary="Update an order by its ID")
    def put(self,request,order_id):
        data=request.data
        order=get_object_or_404(Order,pk=order_id)
        serializer=self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(operation_summary="Delete an order by its ID")
    def delete(self,request,order_id):
        order=get_object_or_404(Order,pk=order_id)
        order.delete()
        return Response({"msg":"order deleted Sucessfully"},status=status.HTTP_200_OK)
    
class OrderStatusUpdateView(generics.GenericAPIView):
    serializer_class=serializers.OrderStatusUpdateSerializer
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Update the status of an order")
    def put(self,request,order_id):
        order=get_object_or_404(Order,pk=order_id)
        data=request.data
        serializer=self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserOrdersView(generics.GenericAPIView):
    serializer_class=serializers.OrderSerializer
    queryset=Order.objects.all()
    
    @swagger_auto_schema(operation_summary="Get all orders made by a specific user")
    def get(self,request,user_id):
            user=User.objects.get(pk=user_id)

            orders=Order.objects.all().filter(customer=user)

            serializer=self.serializer_class(instance=orders,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserOrderDetailView(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailSerializer
    queryset=Order.objects.all()
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Get the detail of an order made by a specific user")
    def get(self,request,user_id,order_id):
        user=User.objects.get(pk=user_id)

        order=Order.objects.all().filter(customer=user).filter(pk=order_id)


        serializer=self.serializer_class(instance=order)

        return Response(data=serializer.data,status=status.HTTP_200_OK)
