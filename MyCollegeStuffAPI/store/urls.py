from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("users", views.UserViewSet)




app_name = 'store'

urlpatterns = [

	url(r'products/$',views.ProductsView.as_view(), name= 'products'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name= 'details'),
	url(r'^login/$', views.custom_login, name ='login'),
    url(r'^logout/$', logout, name ='logout', kwargs = {'next_page': '/store/products'}),
]
