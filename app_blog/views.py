from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View, UpdateView, DeleteView, CreateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import token_generator
from .models import User, Blog
from . forms import SignupForm, LoginForm, ProfileUpdate, BlogForm, CreateBlogForm



class SignUp(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('app_blog:home'))
        form = SignupForm()
        return render(request, 'app_blog/signup.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            print(user.pk)
            print(uidb64)
            domain = get_current_site(request).domain
            link = reverse('app_blog:activate', kwargs={
                           'uidb64': uidb64,
                            'token': token_generator.make_token(user)})
            activate_url = 'http://' + domain + link

            html_file = get_template('app_blog/mail_template.html')
            html_content = html_file.render({'user': user, 'activate_url':activate_url})
            email_subject = 'Activate your account'
            email_body = "email body"
            from_mail = 'sachin.proshore@gmail.com'
            send_to = [form.cleaned_data['email']]
            msg = EmailMultiAlternatives(email_subject, email_body, from_mail, send_to)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            return HttpResponse("<h1>check your mail to active account</h1>")
        else:
            print("Form invalid!")
            return render(request, 'app_blog/signup.html',{'form':form})


class Verification(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            print(user_id)
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return redirect('/login/')
            user.is_active = True
            user.save()
            redirect("/loign/")
        except Exception:
            pass
        return redirect('/login/')


class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('app_blog:home'))
        form = LoginForm()
        return render(request, 'app_blog/login.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(reverse('app_blog:home'))
            else:
                print('Auth crediential do not match!')
        return render(request, 'app_blog/login.html', {'form' : form})


class Logout(View):
    def get(self, request):
        logout(request)
        return  redirect('/login/')


class Home(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all().order_by('-id')
        return render(request, 'app_blog/home.html', {'blogs': blogs})


class BlogDetailView(LoginRequiredMixin, View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        return render(request, 'app_blog/blogdetail.html', {'blog': blog})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_object = get_object_or_404(User, id=request.user.id)
        form = ProfileUpdate(instance=user_object)
        blogs = request.user.blog_set.all()
        return render(request, 'app_blog/profile.html', {'form': form, 'blogs':blogs})

    def post(self, request, *args, **kwargs):
        user_object = get_object_or_404(User, id=request.user.id)
        form = ProfileUpdate(request.POST, instance=user_object)
        if form.is_valid():
            form.save()
            return redirect(f'/crud/detail/{request.user.id}')
        else:
            print('from is invalid')
        blogs = request.user.blog_set.all()
        return render(request, 'app_blog/profile.html', {'form': form, 'blogs': blogs})


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BlogForm
    success_url = '/profile/'
    template_name = 'app_blog/blogupdate.html'
    model = Blog


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = '/profile/'


class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateBlogForm
    template_name = 'app_blog/blogcreate.html'
    success_url = "/profile/"
