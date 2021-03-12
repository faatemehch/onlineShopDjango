from django.urls import path
from .views import (
    ProductList,
    CheapestProducts,
    ExpensiveProducts,
    ActiveProducts,
    NewestProducts,
    product_detail,
    SearchProductView,
    ProductListByCategory
)

urlpatterns = [
    path( 'products', ProductList.as_view(), name='list_products' ),
    path( 'products-cheapest', CheapestProducts.as_view(), name='products-cheapest' ),
    path( 'products-most-expensive', ExpensiveProducts.as_view(), name='products-most-expensive' ),
    path( 'products-active', ActiveProducts.as_view(), name='products-active' ),
    path( 'products-new', NewestProducts.as_view(), name='products-new' ),
    path( 'products/<int:productId>', product_detail, name='product-detail' ),
    path( 'products/search', SearchProductView.as_view(), name='products-search' ),
    path( 'products/<category_name>', ProductListByCategory.as_view(), name='products-category' ),
]
