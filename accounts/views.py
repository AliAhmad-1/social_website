from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView,\
    PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .forms import LoginForm,RegisterForm,UpdateProfileUser
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from accounts.models import MyUser as User
from social_app.models import Post
from.models import Contact
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from social_app.forms import PostModelForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage  





class LoginUser(LoginView):
    template_name='accounts/login.html'
    form_class=LoginForm

    def form_valid(self, form):
        remember_me=form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super(LoginUser,self).form_valid(form)
    

class LogoutUser(LogoutView):
    template_name='accounts/logout.html'
class Register(CreateView):
    template_name='accounts/register.html'
    form_class=RegisterForm
    success_url=reverse_lazy('login')
    def form_valid(self, form):
        user =form.save(commit=False)  
        user.is_active = False  
        user.save()  
        # to get the domain of the current site  
        current_site = get_current_site(self.request)  
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('accounts/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
        to_email = form.cleaned_data.get('email')  
        email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
        email.send()  
        return self.get_success_url()

    def get_success_url(self):
        return HttpResponse('Please confirm your email address to complete the registration')  
def activate(request, uidb64, token):   
    try:  
        uid = force_bytes(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.<a href="http://localhost:8000/accounts/login/"> Login</a>')  
    else:  
        return HttpResponse('Activation link is invalid!')  

@method_decorator(login_required,name='dispatch')
class UserProfileUpdate(UpdateView):
    model=User
    template_name='accounts/profile.html'
    form_class=UpdateProfileUser
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        messages.add_message(self.request,messages.SUCCESS,"Your Profile update successfully")
        return super().form_valid(form)

@login_required
def user_profile(request,user_id):
    posts=Post.objects.filter(user__id=user_id)
    user_detail=User.objects.get(id=user_id)
    followers_count=Contact.objects.filter(user_to=user_detail).count()
    form=PostModelForm()



    followers=Contact.objects.filter(user_from=request.user).values('user_to_id')
    arr_id=[i['user_to_id'] for i in followers]
    follow=False
    if user_id in arr_id:
        follow=True
  
    arr_id.append(request.user.id)
    suggestion=Contact.objects.filter(user_from__in=arr_id).exclude(user_to__in=arr_id).order_by('?')[:5]
    return render(request,'accounts/profile_user.html',{'form':form,'posts':posts,'user':user_detail,'followers':followers_count,'suggestion':suggestion,'follow':follow})
    

    

class Passwordchangeview(PasswordChangeView):
    template_name='accounts/passwordchange.html'
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        messages.add_message(self.request,messages.SUCCESS,"Your password changed successfully")
        return super().form_valid(form)
    

class Password_Reset(PasswordResetView):
    template_name='accounts/passwordreset.html'

class Password_Reset_Done(PasswordResetDoneView):
    template_name='accounts/passwordresetdone.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='accounts/passwordresetconfirm.html'

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name='accounts/passwordresetcomplete.html'