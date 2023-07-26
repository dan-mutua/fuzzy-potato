from django.urls import path
from app import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import *
from django.conf.urls.static import static

urlpatterns = [
 
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.productDetail.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('laptop/', views.financebooks, name='finacebooks'),
    path('bottomwear/', views.mindfulnessBooks, name='mindfull'),
    path('checkout/', views.checkout, name='checkout'),
    path('mindfulness-books/', views.mindfulnessBooks),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='passwordchangedone'),name='passwordchange'),
    path('passwordchange/passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone' ),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password-reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password-reset-done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password-reset-confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password-reset-complete.html'),name='password_reset_complete'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('download-pdf/<int:pdf_file_id>/', views.download_pdf, name='download_pdf'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=static(settings.STATIC_URL,document_root=settings.MEDIA_ROOT)

