"""
Патч для совместимости Django 4.2.7 с Python 3.14
Исправляет ошибку 'super' object has no attribute 'dicts'
"""

import django.template.context

def apply_django_patch():
    """Применяет исправления для Django"""
    
    # Исправление для Context.__copy__
    original_context_copy = django.template.context.Context.__copy__
    
    def fixed_context_copy(self):
        duplicate = original_context_copy(self)
        # Вручную копируем необходимые атрибуты
        if hasattr(self, 'dicts'):
            duplicate.dicts = self.dicts[:]
        if hasattr(self, '_reset_dict'):
            duplicate._reset_dict = self._reset_dict
        return duplicate
    
    django.template.context.Context.__copy__ = fixed_context_copy
    
    print("✅ Патч для Django + Python 3.14 применен")

# Применяем патч при импорте
apply_django_patch()