from django import forms

from book.models import ProductCard, Recipe
from core.fields import CustomCaptchaField
from core.widgets import CustomTimeDurationWidget


class NewProductCardForm(forms.ModelForm):
    shelf_life = forms.DurationField(
        label='Срок годности',
        widget=CustomTimeDurationWidget(show_minutes=False, show_seconds=False),
        required=False
    )
    shelf_life_after_opening = forms.DurationField(
        label='Срок годности после вскрытия упаковки',
        widget=CustomTimeDurationWidget(show_minutes=False, show_seconds=False),
        required=False
    )
    captcha = CustomCaptchaField()

    class Meta:
        model = ProductCard
        fields = ('subcategory', 'name', 'designation', 'shelf_life', 'shelf_life_after_opening',
                  'min_storage_temperature', 'max_storage_temperature',
                  'storage_temperature_unit', 'composition', 'energy_value', 'energy_value_unit',
                  'proteins', 'fats', 'carbohydrates', 'image')


class NewRecipeForm(forms.ModelForm):
    captcha = CustomCaptchaField()

    class Meta:
        model = Recipe
        fields = ('category', 'name', 'people_count', 'recipe', 'energy_value',
                  'energy_value_unit', 'image')
