from wtforms.validators import ValidationError
from model.user import User


class ValidatorMixin:
    @classmethod
    def get_validators(cls):
        validators = []
        for key in cls.__dict__:
            if isinstance(cls.__dict__[key], staticmethod):
                validators.append(getattr(cls, key))
        return validators


def validate_email(form, field):
    if User.get_user_by_email(field.data):
        raise ValidationError('This email address has already been taken.')


def validate_required_checkbox(form, field):
    if not field.data:
        raise ValidationError('You must agree to the terms of service to continue.')


class UsernameValidator(ValidatorMixin):
    # TODO: This validation should be done using AJAX
    @staticmethod
    def is_available(form, field):
        """
        Check if the username already exists in the system.
        """
        if User.get_user(field.data):
            raise ValidationError('This username has already been taken.')

    @staticmethod
    def is_valid(form, field):
        """
        Check if the username is valid. A valid username must contain only lowercase, uppercase and numerical
        characters. Acceptable special characters are: '.' (period) and '_' (underscore).
        """
        invalid_chars = []
        for char in field.data:
            if not ( ord('A') <= ord(char) <= ord('Z') or ord('a') <= ord(char) <= ord('z') or ord('0') <= ord(char) <=
                     ord('9') or ord(char) == ord('.') or ord(char) == ord('_') ):
                invalid_chars.append(char)
        if invalid_chars:
            raise ValidationError('The username contains invalid characters ({}). A username must only contain '
                                  'lowercase, uppercase and numerical characters. Special characters such as the '
                                  'period and the underscore are also accepted.'.format(''.join(invalid_chars)))

    @staticmethod
    def length(form, field):
        char_length = 20
        if len(field.data) > char_length:
            raise ValidationError('The username must not exceed over {} characters.'.format(char_length))


class PasswordValidator(ValidatorMixin):
    # TODO: Check password against haveibeenpwned API
    # TODO: Show how "strong" the user's password is
    @staticmethod
    def length(form, field):
        """
        Validate that the password is at least 8 characters long.
        """
        if len(field.data) <= 8:
            raise ValidationError('The password must be greater than 8 characters.')
        if len(field.data) > 30:
            raise ValidationError('The password must not exceed 30 characters.')

    @staticmethod
    def contains_upper_lower(form, field):
        """
        Validate that the password contains a mix of uppercase and lowercase characters.
        """
        uppercase = False
        lowercase = False
        for char in field.data:
            if ord('A') <= ord(char) <= ord('Z'):
                uppercase = True
            elif ord('a') <= ord(char) <= ord('z'):
                lowercase = True
        if not uppercase or not lowercase:
            raise ValidationError('The password must contain a mix of uppercase and lowercase characters.')

    @staticmethod
    def has_number(form, field):
        """
        Validate that the password contains at least a number character.
        """
        has_num = False
        for char in field.data:
            if ord('0') <= ord(char) <= ord('9'):
                has_num = True
        if not has_num:
            raise ValidationError('The password must contain at least a number.')