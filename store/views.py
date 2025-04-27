from django.shortcuts import render, get_object_or_404, get_list_or_404
from store.models import Category, Product, ProductVariation, Size, Brand
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from store.forms import QuantityForm
from reviews.forms import ReviewForm



# View to display the homepage with top categories and featured products
class HomePageView(View):
    """
    View to render the homepage, showcasing top categories and featured products.
    
    Methods:
        get(request): Renders the homepage with top categories, latest, and popular products.
    """
    def get(self, request):
        # Get top-level categories (no parent)
        top_categories = Category.objects.filter(parent__isnull=True)
        
        # Get the latest active products (limit to 4)
        latest_products = [
            product for product in Product.objects.all().order_by("-created") if product.is_active
        ][:4]
        
        # Get popular active products (limit to 4)
        popular_products = [
            product for product in Product.objects.all().order_by("-created") if product.is_active
        ][:4]

        # Render the homepage with the products and categories
        context = {
            "latest_products": latest_products,
            "popular_products": popular_products,
            "top_categories": top_categories
        }
        return render(request, "index.html", context)


# View to display product details with an option to choose product variations
class ProductDetailPage(View):
    """
    View to display detailed information about a product, including its variations and reviews.
    
    Methods:
        get(request, slug): Renders the product details page.
    """
    template_name = "product-detail.html"
    
    def get(self, request, slug):
        # Initialize form and review form
        form = QuantityForm(initial={"quantity": 1})
        review_form = ReviewForm()
        
        # Get the product object by slug
        product = get_object_or_404(Product, slug=slug)
        
        # Get the product's reviews
        reviews = product.reviews.all()
        reviews_count = len(reviews)
        
        # Determine the selected variation, defaulting to featured if no variant is chosen
        variant_slug = request.GET.get("variant_slug", None)
        if variant_slug is None:
            chosen = product.featured
        else:
            chosen = get_object_or_404(ProductVariation, slug=variant_slug)
        
        # Render the product detail page with context
        context = {
            "chosen": chosen,
            "form": form,
            "review_form": review_form,
            "reviews": reviews,
            "reviews_count": reviews_count,
            "product": product
        }
        return render(request, self.template_name, context)


# View to display a paginated list of products with filtering and sorting options
class ShopPageView(View):
    """
    View to display the shop page with products, categories, and various filters.
    
    Methods:
        get(request): Renders the shop page with filtering, sorting, and pagination.
    """
    template_name = "shop.html"
    
    def get(self, request):
        # Get active products and other necessary data
        products = Product.objects.filter(is_active=True)
        categories = Category.objects.all()
        sizes = Size.objects.all()
        colors = ProductVariation.objects.filter(is_active=True).values_list('color', flat=True).distinct()
        brands = Brand.objects.all()
        
        # Handle sorting by latest, alphabetical, or on sale
        sorting = request.GET.get("sorting", None)
        if sorting:
            if sorting == "latest":
                products = products.order_by("-created")
            elif sorting == "alpha":
                products = products.order_by("name")
            elif sorting == "on_sale":
                products = products.filter(on_sale=True)

        # Handle category filtering
        category_slug = request.GET.get("category", None)
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            if category is None:
                raise ValueError("Category not found")
            else:
                products = products.filter(category=category)
        
        # Handle size filtering
        size = request.GET.get("size", None)
        if size:
            size = get_object_or_404(Size, name=size)
            products = products.filter(variations__size=size)
        
        # Handle color filtering
        color = request.GET.get("color", None)
        if color:
            products = products.filter(variations__color__iexact=color).distinct()
        
        # Handle brand filtering
        brand = request.GET.get("brand", None)
        if brand:
            brand = get_object_or_404(Brand, name=brand)
            products = products.filter(brand=brand)
        
        # Handle search query
        query = request.GET.get("query", None)
        if query:
            products = products.filter(name__icontains=query)
        
        # Pagination setup
        paginator = Paginator(products, 5)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        
        # Render the shop page with context
        context = {
            "products": products,
            "categories": categories,
            "sizes": sizes,
            "colors": colors,
            "brands": brands,
            "page": page
        }
        return render(request, self.template_name, context)