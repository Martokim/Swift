import os.path

from django.db.migrations import serializer
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django_daraja.mpesa.core import MpesaClient
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customers.Serializers import CustomerSerializer, OrderSerializer
from customers.forms import CustomerForm
import os
from django.contrib import messages
from django.shortcuts import get_object_or_404

from customers.models import Customer, Order


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    data = Customer.objects.all()
    context = { 'data': data }
    return render(request,'about.html', context)

#this method is used to put data in the database
def contact(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid(): #django inbuilt function checks for validation
            form.save()
            return redirect('contact') # after user keys in , it redirects back to the same page(contact form)
    else:
          form = CustomerForm() #if it doesn't have a post request , render an empty form
    return render(request, 'contact.html',{'form':form})

def update(request,id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            if 'image' in request.FILES:
                file_name = os.path.basename(request.FILES['image'].name)
                messages.success(request, f'Customer updated successfully! {file_name} uploaded')
            else:
                messages.success(request, 'Customer details updated successfully!')
            return redirect('about')
        else:
            messages.error(request,'Please confirm your changes')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update.html',{'form':form,'customer':customer})

def delete(request,id):
    customer = get_object_or_404(Customer,id=id)

    try:
        customer.delete()
        messages.success(request, f'Customer deleted successfully!')
    except Exception as e:
        messages.error(request,'Customer not deleted!')
    return redirect('about')


@api_view(['GET', 'POST'])
def customersapi(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializers = CustomerSerializer(customers, many=True)
        return JsonResponse(serializers.data, safe=False)  # Fixed: serializers, not serializer
    elif request.method == 'POST':
        serializers = CustomerSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def order_detail(request, id=None):
    # If id is provided, fetch the specific order by id
    if id:
        order = get_object_or_404(Order, id=id)
    else:
        order = None  # No order is found if no id is provided for POST request

    if request.method == 'GET':
        # For GET request, fetch order by id
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'POST':
        # For POST request, create a new order
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        # For PUT and PATCH, update the order
        partial = request.method == 'PATCH'
        serializer = OrderSerializer(order, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # For DELETE, delete the order
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def order_detail(request, id):
#     # Get the specific order by ID
#     order = get_object_or_404(Order, id=id)
#
#     if request.method == 'GET':
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # Handle POST request to create a new order
#         serializer = OrderSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()  # Save the new order to the database
#             return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created order with 201 status
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method in ['PUT', 'PATCH']:
#         # For PUT and PATCH, use `partial=True` for PATCH
#         partial = request.method == 'PATCH'
#         serializer = OrderSerializer(order, data=request.data, partial=partial)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         order.delete()
#         return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


def mpesaapi(request):
    client = MpesaClient()
    phone_number = '0716931752'
    amount = 1
    account_reference ='eMobilis'
    transaction_desc = 'payment for Web Dev'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = client.stk_push(phone_number,amount,account_reference,transaction_desc,callback_url)
    return HttpResponse(response)










