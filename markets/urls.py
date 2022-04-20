"""URL paths for the 'markets' app"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_markets, name='markets'),
    path('<int:market_id>/', views.market_details, name='market_details'),
    path('add/', views.add_market, name='add_market'),
    path('edit/<int:market_id>/', views.edit_market, name='edit_market'),
    path('delete/<int:market_id>/', views.delete_market, name='delete_market'),
    path(
        'delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
        ),
]
