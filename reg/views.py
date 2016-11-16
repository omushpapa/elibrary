from django.shortcuts import get_object_or_404, render, RequestContext, render_to_response
from repo.forms import UserForm, UserEditForm
from reg.forms import MyRegistrationForm
from reg.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.views import generic
from hashids import Hashids
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm

hashids = Hashids(salt='2016-08-18 16:27:22 IiTNmll0 ATn1ViSu', alphabet='123456789abdefghijmdncklopqrstuvwxy0', min_length=7)

def home(request):
    return render(request, 'reg/home.html')

def about(request):
    return render(request, 'reg/about.html')

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('reg:home'))
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            messages.success(request, 'Account created successful')
            return HttpResponseRedirect(reverse('reg:index'))
        
        messages.error(request, 'Resistration failed. Check the listed errors')
    else:
        form = MyRegistrationForm()
        
    return render(request, 'reg/register.html', {
        'form': form,
        })

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('reg:home'))
    if request.method == 'POST':
        user = authenticate(username=request.POST.__getitem__('username'),
            password=request.POST.__getitem__('password'))
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return HttpResponseRedirect(reverse('reg:index'))

        messages.error(request, 'Login failed')

    return render(request, 'reg/login.html', {'form': UserForm()})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return render(request, 'reg/home.html')

@login_required(login_url='/login')
def edit_user(request, pk):
    try:
        pk = hashids.decode(pk)[0]
    except IndexError:
        raise Http404

    user = User.objects.get(pk=pk)

    # Prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserEditForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('website', 'bio', 'phone', 'city', 'country', 'organisation'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserEditForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('reg:profile', args=(hashids.encode(pk),)))

        return render(request, "reg/account_update.html", {
                "noodle": pk,
                "noodle_form": user_form,
                "formset": formset,
            })
    else:
        raise PermissionDenied

def profile(request, pk):
    try:
        pk = hashids.decode(pk)[0]
    except:
        raise Http404
    #user_data = get_object_or_404(User, pk=pk)
    try:
        user_profile = UserProfile.objects.select_related('user').get(user__pk=pk, user__is_active='TRUE')
        user_data = User.objects.get(pk=pk)
    except UserProfile.DoesNotExist or User.DoesNotExist:
        raise Http404("Profile unavailable")
    return render(request, 'reg/viewprofile.html', {
        'user_profile': user_profile,
        'user_data': user_data,
        })

#def reset_pass(request):
#    return password_reset(request,
#            is_admin_site=False,
#            template_name='reg/pass_reset.html',
#            post_reset_redirect='reg/home',
#        )
#
#def reset_confirm(request, uidb64=None, token=None):
#    return password_reset_confirm(request, template_name='reset_confirm.html',
#        uidb36=uidb36, token=token, post_reset_redirect='reg/home')