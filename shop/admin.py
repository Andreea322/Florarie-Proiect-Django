from django.contrib import admin
from .models import Categorie, Floare, Ambalaj, Buchet, TipEveniment, RevistaSezoniera

# Register your models here.

admin.site.register(Categorie)
admin.site.register(Floare)
admin.site.register(Ambalaj)
admin.site.register(Buchet)
admin.site.register(TipEveniment)
admin.site.register(RevistaSezoniera)
