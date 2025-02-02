from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Password must be at least %(min_length)d characters long."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 digit."),
                code='password_no_digit',
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 uppercase letter."),
                code='password_no_upper',
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 lowercase letter."),
                code='password_no_lower',
            )
        if not any(not char.isalnum() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 special character."),
                code='password_no_special',
            )
        
    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters, "
            "including uppercase, lowercase, digits, and special characters."
            % {'min_length': self.min_length}
        )

class CommonPasswordValidator:
    @staticmethod
    def validate(password):
        common_passwords = {
            '123456', 'password', 'qwerty', 'abc123', 'password123',
            'admin', '12345678', 'welcome', 'letmein', 'monkey'
        }
        if password.lower() in common_passwords:
            raise ValidationError(
                _("This password is too common."),
                code='password_too_common',
            )

    @staticmethod
    def get_help_text():
        return _("Your password cannot be a commonly used password.")
