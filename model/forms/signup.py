from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email
from model.forms.validators import UsernameValidator, PasswordValidator, validate_email, validate_required_checkbox


class SignupForm(FlaskForm):
    username = StringField(
        '<strong>Display name</strong>',
        validators=[InputRequired()] + UsernameValidator.get_validators()
    )

    email = StringField(
        '<strong>Email address</strong>',
        validators=[InputRequired(), Email(), validate_email],
        description='The email address is solely used for account management and recovery purposes and will never be '
                    'shown publicly.'
    )

    password = PasswordField(
        '<strong>Password</strong>',
        validators=[
            InputRequired(),
        ] + PasswordValidator.get_validators(),
        description='Use a strong password that is at least 8 characters long with an uppercase character and a '
                    'numerical character.'
    )

    tos = BooleanField(
        'I agree to the <a href="/policies/tos" target="_blank">terms of service</a>.',
        validators=[validate_required_checkbox]
    ) # TODO: can the route not be hardcoded? Prefer to use url_for if possible

    submit = SubmitField('Sign up')


