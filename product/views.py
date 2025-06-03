from django.shortcuts import render
from .models import Product,Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.

def products(request):
    products=Product.objects.all()
    Category.objects.all()
    return render(request,"products.html",{'products':products})


class ProductList(ListView):
    model=Product

class ProductDetailView(DetailView):
    model=Product

class CategoryDetailView(DetailView):
    model=Category
    template_name="category/category.html"
    context_object_name="category"
    slug_field="category_slug"


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        print(context)
        context["products"]=Product.objects.all()
        print(context)
        return context
    