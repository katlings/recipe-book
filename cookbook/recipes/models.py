from django.db import models

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    genre = models.CharField(max_length=64, blank=True, null=True)  # italian, japanese, etc
    dish_type = models.CharField(max_length=64, blank=True, null=True)  # side, dessert, main, etc
    approx_time = models.DurationField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    directions = models.TextField()
    source = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64)

    def __str__(self):
        return "{}: {} ({})".format(self.recipe.name, self.ingredient.name, self.quantity)
