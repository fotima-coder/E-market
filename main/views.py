from django.shortcuts import render,redirect,get_object_or_404
from django.views import View


from django.contrib.auth import get_user_model

from main.models import *

User = get_user_model()



class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:

            categories = Category.objects.all()
            ads = Ad.objects.all()
            context = {
                'categories': categories,
                'ads': ads,
            }
            return render(request, 'index.html', context)
        return render(request, 'index-unauth.html')

class CategoryView(View):
    def get(self, request, slug):
        if request.user.is_authenticated and request.user.confirmed:
            category = get_object_or_404(Category, slug=slug)
            sub_categories = category.subcategory_set.filter(category=category).order_by('-image')
            context = {
                'category': category,
                'sub_categories': sub_categories,
            }
            return render(request, 'category.html', context)
        return redirect('login')


class ProductsView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            products = Product.objects.all()

            query_view = request.GET.get('view')

            query_sub = request.GET.get('sub-category')
            sub_category = None
            if query_sub:
                sub_category = get_object_or_404(SubCategory, slug=query_sub)
                products = products.filter(sub_category=sub_category)

            context = {
                'products': products,
                'query_sub': query_sub,
                'sub_category': sub_category,
                'query_view': query_view,
            }

            if query_view and query_view.lower() == 'large':
                return render(request, 'products-large.html', context)
            return render(request, 'products-grid.html', context)
        return redirect('login')