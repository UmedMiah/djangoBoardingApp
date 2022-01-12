import bleach
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from boarding.functions import validate

from .models import Products, UserAccess
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView


User = get_user_model() # noqa

# This serves the user status page, only if that user is logged in


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
        # This passes to the template, a filtered list of products the user has access to
        return context

    def test_func(self):
        # This ensure only the user the page belongs to or Admin can view the status
        if str(self.request.user) == str(self.kwargs['username']):
            return True
        else:
            return self.request.user.is_superuser


user_detail_view = UserDetailView.as_view()


# Code below is self documenting -> object ID is passed, and deleted
class RemoveAccess(DeleteView):
    model = UserAccess

    def get_context_data(self, **kwargs):
        context = super(RemoveAccess, self).get_context_data(**kwargs)
        context['target_id'] = self.object.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('user', kwargs={'username': self.object.user})

    template_name = 'remove_access.html'


remove_access = RemoveAccess.as_view()


class Index(TemplateView):
    template_name = "index.html"


index = Index.as_view()


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User

    template_name = "update_detail.html"

    fields = [
        "email",
    ]

    # This ensure only the user the page belongs to or Admin can edit the email
    def test_func(self):
        if str(self.request.user.pk) == str(self.kwargs['pk']):
            return True
        else:
            return self.request.user.is_superuser

    def form_valid(self, form):
        # Check for email duplicate and format using validate function.
        email = form.cleaned_data['email']
        emailCheck = validate('email', email)
        if User.objects.filter(email=email).exists():
            messages.info(self.request, 'Email already used')
            return super(UserUpdateView, self).form_invalid(form)
        elif not emailCheck == 'Pass':
            messages.info(self.request, emailCheck)
            return super(UserUpdateView, self).form_invalid(form)
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.INFO, 'Invalid Email')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.INFO, 'Email updated')
        return reverse_lazy('user', kwargs={'username': self.object.username})


user_update_view = UserUpdateView.as_view()


def register(request):
    # Each field is validated using the validate function
    # If validate function fails, valid is set to false
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
                    email=bleach.clean(email),
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
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def team(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'team.html', {'users': users})
    else:
        messages.info(request, 'Page does not exist')
        redirect_response = render(request, 'index.html')
        redirect_response.status_code = 302
        return redirect_response


# Below code ensures that only admins can add access.
# Initally verifies that the user and product exist, and that there is no duplicates
def addaccess(request, userPK, productPK):

    if not request.user.is_superuser:
        messages.info(request, 'Page does not exist')
    elif not User.objects.filter(pk=userPK).exists() or not Products.objects.filter(pk=productPK).exists():
        messages.info(request, 'User or product does not exist')
        return redirect('/')
    elif UserAccess.objects.filter(product=productPK).filter(user=userPK).exists():
        messages.info(request, 'Access has already been granted')
        username = str(User.objects.filter(pk=userPK)[0])
        return redirect('user', {'username': username})
    elif request.method == 'POST':
        username = str(User.objects.filter(pk=userPK)[0])
        useraccess = UserAccess.objects.create(user_id=userPK, product_id=productPK)
        useraccess.save()
        messages.info(request, 'User access added')
        return redirect('user', username)
    else:
        username = str(User.objects.filter(pk=userPK)[0])
        return render(request, 'add_access.html', {'username': username})
