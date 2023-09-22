from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("new_auction", views.new_auction_view, name="new_auction"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:auction_title>", views.auction, name="auction"),
    path("no_auction", views.no_auction, name="no_auction"),
]
