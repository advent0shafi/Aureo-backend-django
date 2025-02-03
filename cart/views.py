from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
import uuid

class CartAPIView(APIView):
    permission_classes = [AllowAny]  # Allow both authenticated and guest users

    def get_or_create_cart(self, request):
        """
        Helper method to get or create a cart for the user or guest.
        """
        cart = None
        guest_id = None

        if request.user.is_authenticated:
            # Get or create cart for logged-in user
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # Get or create cart for guest
            guest_id = request.headers.get('X-Guest-ID')
            if not guest_id:
                guest_id = str(uuid.uuid4())
                request.session['guest_id'] = guest_id
                request.session.modified = True  # Mark session as modified

            cart, created = Cart.objects.get_or_create(guest_id=guest_id)

        return cart, guest_id

    def get(self, request):
        """
        Handle GET request to retrieve the cart.
        """
        cart, _ = self.get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST request to add an item to the cart.
        """
        cart, guest_id = self.get_or_create_cart(request)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            # Check if the product is already in the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                # Update quantity if the product is already in the cart
                cart_item.quantity += quantity
                cart_item.save()

            # Update cart's updated_at timestamp
            cart.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Handle PUT request to update a cart item.
        """
        cart, _ = self.get_or_create_cart(request)
        try:
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update cart's updated_at timestamp
            cart.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """
        Handle PATCH request for partial updates to a cart item.
        """
        cart, _ = self.get_or_create_cart(request)
        try:
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update cart's updated_at timestamp
            cart.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Handle DELETE request to remove a cart item.
        """
        cart, _ = self.get_or_create_cart(request)
        try:
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        # Update cart's updated_at timestamp
        cart.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)