from django.urls import path
from . import views

# hhtp://localhost/board/
app_name = "board"
urlpatterns = [
    path("", views.board_list, name="board_list"),
    path("write/", views.board_write, name="board_write"),
    path("detail/<int:pk>/", views.board_detail, name="board_detail"),
]
