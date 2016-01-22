from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import login,logout
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.authtoken.models import Token

from .models import Product, UserForm
from .serializers import ProductSerializer, UserSerializer
from .permissions import IsAuthenticatedOrAnon
from django.views import generic

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from .forms import LoginForm

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('store:products'))
    return login(request, template_name='store/login.html')


class ProductsView(generic.ListView):
    template_name='store/products.html'
    context_object_name='item_list'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all().reverse()

class DetailsView(generic.DetailView):
    model = Product
    template_name = 'store/details.html'

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ("product", )

    def destroy(self, request, *args, **kwargs):
        """
        Only allow stuff to be delete if they belong to user.
        """
        user = request.user
        product = self.get_object()
        if product.student_id == user.id:
            return super(ProductViewSet, self).destroy(request, *args, **kwargs)
        else:
            data = {"detail": "Unauthorized for operation"}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint for User.
    Doesn't allow DELETE operation. In order to delete account,
    user must do it from web interface.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrAnon, )

    @detail_route()
    def selling(self, request, *args, **kwargs):
        """
        Retrieve all things the current user is selling
        """
        user = self.get_object()
        queryset = Product.objects.filter(student_id=user.pk)
        # Serialize stuff, tell that there is many objects to serialize
        return Response(ProductSerializer(queryset, many=True).data)

    def create(self, request, *args, **kwargs):
        """
        Create a new user \o/
        """
        # print(request.data)
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            # Manually input data since "**validated_data" could contain
            # other (unsecured) things
            user = User.objects.create_user(
                userSerializer.validated_data['email'],
                email=userSerializer.validated_data['email'],
                first_name=userSerializer.validated_data['first_name'],
                last_name=userSerializer.validated_data['last_name']
            )
            user.set_password(userSerializer.validated_data['password'])
            user.save()
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key}, status.HTTP_201_CREATED)
        return Response(userSerializer.errors, status.HTTP_400_BAD_REQUEST)
