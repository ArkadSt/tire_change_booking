from django.urls import path
from .views import get_tire_change_times, book_tire_change_time, get_workshops

urlpatterns = [
    path("times/", get_tire_change_times, name="get_tire_change_times"),
    path("book/", book_tire_change_time, name="book_tire_change_time"),
    path("workshops/", get_workshops, name="get_workshops"),

]