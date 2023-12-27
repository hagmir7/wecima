from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.views.generic import DetailView, UpdateView, UpdateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "/")
            if next_url:
                return redirect(next_url)
            if user.is_superuser:
                return redirect("/dashboard")
            else:
                return redirect("home")
        else:
            return render(
                request, "auth/login.html", {"error": "Authentification invalide"}
            )
    else:
        return render(
            request,
            "auth/login.html",
            {
                "title": "تسجيل الدخول إلى ويسيما",
                "description": "يمكنك الأن تسجيل الدخول إلى ويسيما ومشاركة منشوراتك والتفاعل معها, الحصول على أخر أخبار الأفلام والمسلسلات",
            },
        )


# REGISTER
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    else:
        form = UserCreationForm()
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                form.cleaned_data["username"]
                new_user.email
                new_user.save()
                if new_user is not None:
                    if new_user.is_active:
                        login(request, new_user)
                        next_url = request.GET.get("next", "/")
                        if next_url:
                            return redirect(next_url)
                        return redirect("home")

                return redirect("login")
    context = {"title": _("Register"), "form": form, "title": "إنشاء حساب وتسجيل الدخول إلى ويسيما"}
    return render(request, "auth/register.html", context)


class ProfileView(DetailView):
    model = Profile
    template_name = "profile/posts.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, *arge, **kwargs):
        context = super(ProfileView, self).get_context_data(*arge, **kwargs)
        page = get_object_or_404(Profile, slug=self.kwargs["slug"])
        description = _(
            "You can join now to connect with your  friends and enjoy your books and courses register now"
        )
        title = f"{page.user.first_name} {page.user.last_name}"

        context["page"] = page
        context["title"] = title
        context["description"] = description
        context["iamge"] = page.avatar.url
        return context


@login_required
def ProfileUpdate(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = UpdateProfile(instance=profile)
    if request.method == "POST":
        if request.user == profile.user:
            form = UpdateProfile(
                request.POST, instance=request.user.profile, files=request.FILES
            )
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated!")
                return redirect("profile_update", id=profile.id)
        else:
            return redirect("/")

    context = {"page": profile, "title": _("Update Profile")}

    return render(request, "profile/update_profile.html", context)


@login_required
class ProfileViewUpdate(UpdateView):
    model = Profile
    template_name = "profile/update_profile.html"
    form_class = UpdateProfile

    def get_context_data(self, *arge, **kwargs):
        context = super(ProfileViewUpdate, self).get_context_data(*arge, **kwargs)
        page = get_object_or_404(Profile, id=self.kwargs["pk"])
        title = _("Update Profile")
        context["page"] = page
        context["title"] = title
        return context


@login_required
def user_update_info(request):
    confirm = False
    if request.method == "POST":
        form = UserUpdateInfo(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            confirm = True
    else:
        form = UserUpdateInfo(instance=request.user)
    context = {"form": form, "confirm": confirm, "title": _("Contact information")}
    return render(request, "profile/user_update_info.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "profile/change-password.html", {"form": form})


def posword_reset_done(request):
    context = {"title": _("Password reset has been sent")}
    return render(request, "password_reset/reset_password_done.html", context)


def settings(request):
    return render(request, "settings.html")
