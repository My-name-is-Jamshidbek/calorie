import datetime
from django.db.models import Sum, F, ExpressionWrapper, FloatField, Case, When
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Cart

@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id)
    grams = int(request.POST.get('grams', 0))

    if grams <= 0:
        return redirect('home')  # Redirect or handle invalid gram input

    cart_item = Cart.objects.create(user=request.user, food=food, gram=grams)
    cart_item.save()


    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    else:
        return redirect('home')


from django.views.decorators.http import require_POST


def cart(request):
    date_input = request.GET.get('date')

    if date_input:
        date = parse_date(date_input)
        if date:
            start_day = datetime.datetime.combine(date, datetime.time.min)
            end_day = datetime.datetime.combine(date, datetime.time.max)
            foods = Cart.objects.filter(created_at__range=(start_day, end_day))
            total_calories = foods.aggregate(
                total_calories=Sum(
                    Case(
                        When(gram__gt=0, then=F('food__calories') * F('gram') / F('food__serving')),
                        default=F('food__calories'),
                        output_field=FloatField()
                    )
                )
            )['total_calories']
        else:
            foods = Cart.objects.filter(user=request.user).all()[::-1]
            total_calories = False
    else:
        foods = Cart.objects.filter(user=request.user).all()[::-1]
        total_calories = False

    return render(request, 'cart.html', {'foods': foods, 'date':
                                         date_input, 'total_calories':total_calories})
