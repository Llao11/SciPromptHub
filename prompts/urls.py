from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_prompts, name="list_prompts"),
    path("add/", views.add_prompt, name="add_prompt"),
    path("api/prompts/", views.prompt_list_api, name="primpt_list_api"),
    path("prompt/<int:pk>/", views.prompt_detail, name="prompt_detail"),
    path("delete/<int:pk>/", views.delete_prompt, name="delete_prompt"),
]
