from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from boarding.functions import validate

from .models import Products, UserAccess
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView


User = get_user_model() # noqa


class UserDetailView(UserPassesTestMixin, DetailView):

    model = User
    products = Products.objects.all()
    useraccess = UserAccess.objects.all()
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products

        userkey = User.objects.filter(username=self.kwargs['username'])
        filteredAccess = UserAccess.objects.filter(user=userkey[0])

        context["products"] = products
        context["useraccess"] = filteredAccess
        return context

    def test_func(self):
        if str(self.request.user) == str(self.kwargs['username']):
            return True
        else:
            return self.request.user.is_superuser


user_detail_view = UserDetailView.as_view()


class RemoveAccess(DeleteView):
    model = UserAccess

    def get_context_data(self, **kwargs):
        context = super(RemoveAccess, self).get_context_data(**kwargs)
        print(self.object.user)
        context['target_id'] = self.object.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('user', kwargs={'username': self.object.user})

    template_name = 'remove_access.html'


remove_access = RemoveAccess.as_view()


class Index(TemplateView):
    template_name = "index.html"


index = Index.as_view()


def register(request):
    if request.method == 'POST':

        valid = True

        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        passwordCheck = validate('password', password)
        if not password == repeatPassword:
            messages.info(request, 'Password did not match')
            valid = False
        elif not passwordCheck == 'Pass':
            messages.info(request, passwordCheck)
            valid = False

        username = request.POST['username']
        usernameCheck = validate('username', username)
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already used')
            valid = False
        elif not usernameCheck == 'Pass':
            messages.info(request, usernameCheck)
            valid = False

        firstname = request.POST['firstname']
        firstnameCheck = validate('name', firstname)
        if not firstnameCheck == 'Pass':
            messages.info(request, firstnameCheck)
            valid = False

        surname = request.POST['surname']
        surnameCheck = validate('name', surname)
        if not surnameCheck == 'Pass':
            messages.info(request, surnameCheck)
            valid = False

        email = request.POST['email']
        emailCheck = validate('email', email)
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already used')
            valid = False
        elif not emailCheck == 'Pass':
            messages.info(request, emailCheck)
            valid = False

        if not valid:
            return redirect('register')
        elif valid:
            user = User.objects.create_user(
                    username=username,
                    first_name=firstname,
                    last_name=surname,
                    email=email,
                    password=password)
            user.save()
            return redirect('login')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username and or password is invalid')
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def team(request):
    users = User.objects.all()
    return render(request, 'team.html', {'users': users})


def addaccess(request, userPK, productPK):
    username = str(User.objects.filter(pk=userPK)[0])

    if not request.user.is_superuser:
        messages.info(request, 'Page does not exist')
    elif not User.objects.filter(pk=userPK).exists() or not Products.objects.filter(pk=productPK).exists():
        messages.info(request, 'User or product does not exist')
        return redirect('user', {'username': username})
    elif UserAccess.objects.filter(product=productPK).filter(user=userPK).exists():
        messages.info(request, 'Access has already been granted')
        return redirect('user', {'username': username})

    if request.method == 'POST':
        useraccess = UserAccess.objects.create(user_id=userPK, product_id=productPK)
        useraccess.save()
        messages.info(request, 'User access added')
        return redirect('user', username)
    else:
        return render(request, 'add_access.html', {'username': username})
