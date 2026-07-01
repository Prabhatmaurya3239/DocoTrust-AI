"""Forms for registration, profile editing, and authentication."""
from __future__ import annotations

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import Profile

_INPUT_CLASS = "form-control form-control-lg"


class BootstrapMixin:
    """Apply consistent Bootstrap styling to all form widgets."""

    def _style_widgets(self) -> None:
        for name, field in self.fields.items():  # type: ignore[attr-defined]
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = (existing + " form-check-input").strip()
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = (existing + " form-select").strip()
            else:
                widget.attrs["class"] = (existing + " " + _INPUT_CLASS).strip()
            widget.attrs.setdefault("placeholder", field.label or name)


class RegisterForm(BootstrapMixin, UserCreationForm):
    """User registration form with email and name capture."""

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._style_widgets()

    def clean_email(self) -> str:
        """Ensure the email address is unique across users."""
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email exists.")
        return email

    def save(self, commit: bool = True) -> User:
        """Persist the user with normalized email and names."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user


class LoginForm(BootstrapMixin, AuthenticationForm):
    """Styled authentication form."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._style_widgets()


class UserUpdateForm(BootstrapMixin, forms.ModelForm):
    """Edit core ``User`` fields from the profile page."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._style_widgets()

    def clean_email(self) -> str:
        """Ensure the email remains unique (excluding the current user)."""
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An account with this email exists.")
        return email


class ProfileUpdateForm(BootstrapMixin, forms.ModelForm):
    """Edit extended profile information."""

    class Meta:
        model = Profile
        fields = ("avatar", "organization", "job_title", "bio", "theme")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._style_widgets()
