from django.urls import path,include
from . import views
urlpatterns = [
    # path('accounts/',include('django.contrib.auth.urls')),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('logout/',views.LogoutUser.as_view(),name='logout'),
    path("register/",views.Register.as_view(), name="register"),
    path("profile/update/<int:pk>",views.UserProfileUpdate.as_view(), name="profile_update"),
        path("profile/<int:user_id>",views.user_profile, name="profile_user"),
    path('passwordchange/',views.Passwordchangeview.as_view(),name='passwordchange'),
    path("password_reset/", views.Password_Reset.as_view(), name="password_reset"),
    path("password_reset/done/",views.Password_Reset_Done.as_view(),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",views.MyPasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("reset/done/",views.MyPasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
