import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Cart


def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'welcome.html')


def home(request):
    if request.user.is_authenticated:
        food_type = request.GET.get('food_type', None)
        print(food_type)
        if food_type:
            food_items = FoodItem.objects.filter(food_type=food_type).all()
        else:
            food_items = FoodItem.objects.all()  # Or handle differently if no type is specified

        query = request.GET.get('query', '')
        if query:
            food_items = FoodItem.objects.filter(name__icontains=query)

        return render(request, 'home.html', context={'foods': food_items, 'query': query, 'food_type': food_type})
    else:
        return render(request, 'welcome.html')


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id)
    cart_item = Cart.objects.create(user=request.user, food=food)
    cart_item.save()
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    else:
        return redirect('home')


def cart(request):
    date_input = request.GET.get('date')

    if date_input:
        date = parse_date(date_input)
        if date:
            start_day = datetime.datetime.combine(date, datetime.time.min)
            end_day = datetime.datetime.combine(date, datetime.time.max)
            foods = Cart.objects.filter(created_at__range=(start_day, end_day))
        else:
            foods = Cart.objects.filter(user=request.user).all()[::-1]

    else:
        foods = Cart.objects.filter(user=request.user).all()[::-1]
    return render(request, 'cart.html', {'foods': foods, 'date':
                                         date_input})
