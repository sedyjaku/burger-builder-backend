from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from api.models import Burger, Ingredient, Address, Order


class SimpleUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        always_return_data = True


    def hydrate(self,bundle):
        if 'id' not in bundle.data.keys():
            user = User.objects.get(username = bundle.data['username'])
            if user is None:
                if 'password' not in bundle.data.keys():
                    bundle.data['password'] = 'RandomPassword'
            else:
                bundle.data['id'] = user.id
        else:
            user = User.objects.get(id = bundle.data['id'])
        bundle.obj = user
        return bundle

class UserResource(ModelResource):
    orders = fields.ToManyField('api.api.OrderResource', 'orders',  null=True, blank=True, readonly=True )
    address = fields.OneToOneField('api.api.AddressResource', 'address', full=True, null=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle):
        data_keys = bundle.data.keys()
        if 'id' not in data_keys:
            exists = User.objects.filter(username = bundle.data['username']).exists()
            if not exists:
                if 'password' not in bundle.data.keys():
                    bundle.data['password'] = 'RandomPassword'
            else:
                user = User.objects.get(username = bundle.data['username'])
                bundle.data['id'] = user.id
        else:
            user = User.objects.get(id = bundle.data['id'])
        # bundle.obj=user
        # if 'address' in bundle.data.keys():
        #     bundle.data['address']['user'] = bundle.obj
        if 'address' in data_keys:
            bundle.data['address']['user'] = bundle.obj
        return bundle

    def dehydrate(self, bundle):
        return bundle


class AddressResource(ModelResource):
    # user = fields.OneToOneField(UserResource, 'user')

    class Meta:
        queryset = Address.objects.all()
        resource_name = 'address'
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle):
        return bundle

    def dehydrate(self, bundle):
        return bundle

class OrderResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    burgers = fields.ToManyField('api.api.BurgerResource', 'burgers', full=True)

    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle):
        burgers = bundle.data['burgers']
        for burger in burgers:
            burger['order'] = bundle.obj
        return bundle

    def dehydrate(self, bundle):
        return bundle

class BurgerResource(ModelResource):
    order = fields.ForeignKey(OrderResource, 'order')
    ingredients = fields.ToManyField('api.api.IngredientResource', 'ingredients', full=True)


    class Meta:
        queryset = Burger.objects.all()
        resource_name = 'burger'
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle):
        ingredients = bundle.data['ingredients']
        for ing in ingredients:
            ing['burger'] = bundle.obj
        return bundle

    def dehydrate(self, bundle):
        return bundle



class IngredientResource(ModelResource):
    burger = fields.ToOneField(BurgerResource, 'burger')

    class Meta:
        queryset = Ingredient.objects.all()
        resource_name = 'ingredient'
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle):
        return bundle

    def dehydrate(self, bundle):
        return bundle

    # def full_hydrate(self, bundle):
    #     return bundle

    def dispatch_list(self, request, **kwargs):
        return

    def alter_deserialized_list_data(self, request, data):
        return

    def obj_create(self, bundle, **kwargs):
        return
