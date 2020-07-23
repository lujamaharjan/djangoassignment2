from django.urls import path
from .views import *


app_name = 'app_blog'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', Verification.as_view(), name='activate'),
    path('', Home.as_view(), name='home'),
    path('blog-detail/<int:blog_id>/', BlogDetailView.as_view(), name="blog_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("blog-update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update"),
    path("blog-delete/<int:pk>", BlogDeleteView.as_view()),
    path("blog-create/", BlogCreateView.as_view())
]