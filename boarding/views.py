from django.shortcuts import redirect, render

from .models import Products, UserAccess
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, DeleteView, FormView

User = get_user_model()


class UserDetailView(UserPassesTestMixin, DetailView):
    model = User
    products = Products.objects.all()
    useraccess = UserAccess.objects.all()
    slug_field = "username"
    slug_url_kwarg = "username" 

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        products = self.products
        # useraccess = self.useraccess

        userkey= User.objects.filter(username=self.kwargs['username'])
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

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()

class RemoveAccess(DeleteView):
    model = UserAccess
    success_url = reverse_lazy('team')
    template_name = 'remove_access.html'

remove_access = RemoveAccess.as_view()

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['uname']
        firstname = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['mail']
        password = request.POST['psw']
        rpassword = request.POST['rpsw']

        if password == rpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,first_name=firstname ,last_name=surname ,email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not the same')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid login')
            return redirect('login')
        
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def team(request):
    users = User.objects.all()
    return render(request, 'team.html', {'users': users})

def addaccess(request, userPK, productPK):
    if not request.user.is_superuser:
        messages.info(request, 'Page does not exist')
    elif not User.objects.filter(pk = userPK).exists() or not Products.objects.filter(pk = productPK).exists():
        messages.info(request, 'User or product does not exist')
        return redirect('team')
    elif  UserAccess.objects.filter(product=productPK).filter(user=userPK).exists():
        messages.info(request, 'Access has already been granted')
        return redirect('team')

    if request.method == 'POST':
        useraccess = UserAccess.objects.create(user_id=userPK, product_id=productPK)
        useraccess.save()
        messages.info(request, 'User access added')
        return redirect('team')
    else:
        return render(request, 'add_access.html')
        