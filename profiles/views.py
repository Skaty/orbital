from django.contrib.auth import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView

from profiles.models import Preferences


class ProfileDetailView(DetailView):
    model = models.User
    template_name = 'profiles/profile_detail.html'


class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password != confirm:
            raise forms.ValidationError(
                'Passwords do not match!'
            )


class TimezonePreferenceForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['timezone']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


@method_decorator(login_required, name='dispatch')
class PreferencesDisplay(TemplateView):
    template_name = 'profiles/preferences_form.html'

    def get_context_data(self, **kwargs):
        pref_instance, create = Preferences.objects.get_or_create(user=self.request.user)
        forms = [
            {
                'title': 'Update Preferences',
                'form': TimezonePreferenceForm(instance=pref_instance),
                'url': reverse_lazy('profiles:preferences-update')
            },
            {
                'title': 'Profile',
                'form': ProfileChangeForm(instance=self.request.user),
                'url': reverse_lazy('profiles:profile-update')
            }
        ]

        if self.request.user.has_usable_password():
            forms += [
                {
                    'title': 'Change Password',
                    'form': PasswordChangeForm(),
                    'url': reverse_lazy('profiles:password-update')
                }
            ]

        kwargs['forms'] = forms

        return super(PreferencesDisplay, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class PasswordUpdateView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('homepage')
    template_name = 'profiles/single_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['formtitle'] = 'Change Password'
        return super(PasswordUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['password'])
        user.save()

        return super(PasswordUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PreferencesUpdateView(FormView):
    form_class = TimezonePreferenceForm
    success_url = reverse_lazy('projects:project-list')
    template_name = 'profiles/single_form.html'

    def get_context_data(self, **kwargs):
        kwargs['formtitle'] = 'Update Preferences'
        return super(PreferencesUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        return super(PreferencesUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    form_class = ProfileChangeForm
    success_url = reverse_lazy('projects:project-list')
    template_name = 'profiles/single_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['formtitle'] = 'Profile'
        return super(ProfileUpdateView, self).get_context_data(**kwargs)