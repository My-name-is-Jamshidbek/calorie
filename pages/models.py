from django.db import models
from django.conf import settings


class FoodType(models.TextChoices):
    FRUIT = 'FRUIT', 'Fruit'
    MEAT = 'MEAT', 'Meat'
    FOOD = 'FOOD', 'Food'
    VEGETABLE = 'VEGETABLE', 'Vegetable'


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    serving = models.CharField(max_length=100)
    calories = models.IntegerField()
    food_type = models.CharField(
        max_length=10,
        choices=FoodType.choices,
        default=FoodType.FOOD
    )
    image = models.ImageField(upload_to='food_images/')  # Specify the directory for uploaded images

    def __str__(self):
        return f"{self.name} ({self.serving})"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='cart_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.food.name}'
