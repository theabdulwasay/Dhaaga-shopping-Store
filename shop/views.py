import json
import os
import uuid
import logging

from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Product, Fabric, ChatLog, Order
from .cart import Cart
from .forms import CheckoutForm, ContactForm

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are the customer support assistant for DHAAGA, a Pakistani cloth brand "
    "selling unstitched and ready-to-wear fabric (khaddar, lawn, linen) sourced from "
    "handloom weavers. Be warm, concise (2-4 sentences), and helpful. You can discuss "
    "fabric types, sizing/metres needed for suits, care instructions, delivery within "
    "Pakistan, and pricing in PKR. Delivery takes 3-5 business days across Pakistan."
)


def home(request):
    products = Product.objects.filter(is_active=True)[:6]
    fabrics = Fabric.objects.all()
    return render(request, "shop/home.html", {"products": products, "fabrics": fabrics})


def product_list(request):
    products = Product.objects.filter(is_active=True)
    fabric_slug = request.GET.get("fabric")
    if fabric_slug:
        products = products.filter(fabric__slug=fabric_slug)
    fabrics = Fabric.objects.all()
    return render(request, "shop/product_list.html", {"products": products, "fabrics": fabrics, "active_fabric": fabric_slug})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "shop/product_detail.html", {"product": product})


@require_POST
def cart_add(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        if not product.is_active:
            messages.error(request, "This product is not available.")
            return redirect(request.POST.get("next", "product_list"))
        
        if not product.in_stock:
            messages.error(request, f"Sorry, {product.name} is out of stock.")
            return redirect(request.POST.get("next", "product_list"))
        
        cart = Cart(request)
        qty = int(request.POST.get("quantity", 1))
        
        if qty <= 0:
            messages.error(request, "Quantity must be at least 1.")
            return redirect(request.POST.get("next", "product_list"))
        
        if qty > product.stock:
            messages.error(request, f"Only {product.stock} items available.")
            return redirect(request.POST.get("next", "product_list"))
        
        cart.add(product, qty)
        messages.success(request, f"Added {qty} x {product.name} to your cart.")
        logger.info(f"Added {qty} x {product.name} to cart")
        return redirect(request.POST.get("next", "cart_detail"))
    except ValueError:
        messages.error(request, "Invalid quantity.")
        return redirect(request.POST.get("next", "product_list"))
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect(request.POST.get("next", "product_list"))


@require_POST
def cart_remove(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)
        messages.success(request, f"Removed {product.name} from your cart.")
        logger.info(f"Removed {product.name} from cart")
        return redirect("cart_detail")
    except Exception as e:
        logger.error(f"Error removing from cart: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"cart": cart})


@transaction.atomic
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty — add something from the collection first.")
        return redirect("product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                order = form.save()
                
                # Check stock availability before creating order
                for item in cart:
                    product = item["product"]
                    quantity = item["quantity"]
                    if product.stock < quantity:
                        raise ValidationError(f"Insufficient stock for {product.name}")
                
                # Create order items and update stock
                for item in cart:
                    product = item["product"]
                    quantity = item["quantity"]
                    order.items.create(
                        product=product,
                        quantity=quantity,
                        unit_price=item["price"],
                    )
                    # Update stock
                    product.stock -= quantity
                    product.save()
                
                cart.clear()
                logger.info(f"Order #{order.id} created for {order.full_name}")
                messages.success(request, f"Order #{order.id} placed successfully!")
                return redirect("order_success", order_id=order.id)
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                logger.error(f"Checkout error: {e}")
                messages.error(request, "An error occurred while processing your order. Please try again.")
    else:
        form = CheckoutForm()

    return render(request, "shop/checkout.html", {"form": form, "cart": cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_success.html", {"order": order})


def order_track(request):
    order_id = request.GET.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except (Order.DoesNotExist, ValueError):
            messages.error(request, "Order not found. Please check your order ID.")
    return render(request, "shop/order_track.html", {"order": order})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Contact message from {form.cleaned_data['name']}")
                messages.success(request, "Thanks — we'll get back to you soon.")
                return redirect("contact")
            except Exception as e:
                logger.error(f"Contact form error: {e}")
                messages.error(request, "An error occurred. Please try again.")
    else:
        form = ContactForm()
    return render(request, "shop/contact.html", {"form": form})


@csrf_exempt
@require_POST
def chat_api(request):
    """
    Proxies chat messages to the Anthropic API using a server-side API key
    (set ANTHROPIC_API_KEY as an environment variable). Logs each turn to ChatLog.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.warning("Invalid chat request body")
        return JsonResponse({"error": "Invalid request body."}, status=400)

    user_message = (payload.get("message") or "").strip()
    history = payload.get("history") or []
    if not user_message:
        return JsonResponse({"error": "Message is required."}, status=400)

    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key or str(uuid.uuid4())

    try:
        ChatLog.objects.create(session_key=session_key, role="user", message=user_message)
    except Exception as e:
        logger.error(f"Error logging user message: {e}")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        reply = (
            "The chatbot isn't fully wired up yet — ask the site owner to set the "
            "ANTHROPIC_API_KEY environment variable on the server to enable live replies."
        )
        try:
            ChatLog.objects.create(session_key=session_key, role="bot", message=reply)
        except Exception as e:
            logger.error(f"Error logging bot message: {e}")
        return JsonResponse({"reply": reply, "configured": False})

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        messages_payload = history + [{"role": "user", "content": user_message}]
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=messages_payload,
        )
        reply = "".join(block.text for block in response.content if block.type == "text").strip()
        if not reply:
            reply = "Sorry, I couldn't put together a reply just now — please try again."
    except Exception as exc:
        logger.error(f"Anthropic API error: {exc}")
        reply = "Something went wrong reaching support. Please try again shortly."

    try:
        ChatLog.objects.create(session_key=session_key, role="bot", message=reply)
    except Exception as e:
        logger.error(f"Error logging bot message: {e}")
    return JsonResponse({"reply": reply, "configured": True})
