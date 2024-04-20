from app.schemas.user import (
    User, TokenData, UserLogin, UserOutput, FormChangePassword,
    FormChangeEmail
)
from datetime import datetime
import pytest


def test_user_schema():
    user = User(
        username='corso',
        password='password',
        email='carlos@email.com',
        is_staff=False,
    )

    assert user.model_dump() == {
        'username': 'corso',
        'password': 'password',
        'email': 'carlos@email.com',
        'is_staff': False
    }


def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(
            username=1234,
            password='password',
            email='carlos@email.com',
            is_staff=False,
        )


def test_user_schema_invalid_password():
    with pytest.raises(ValueError):
        user = User(
            username='corso',
            password={'foo': 'bar'},
            email='carlos@email.com',
            is_staff=False,
        )


def test_user_schema_invalid_email():
    with pytest.raises(ValueError):
        user = User(
            username='corso',
            password='password',
            email='carlos@email',
            is_staff=False,
        )


def test_user_schema_invalid_is_staff():
    with pytest.raises(ValueError):
        user = User(
            username='corso',
            password='password',
            email='carlos@email.com',
            is_staff=None
        )


def test_tokendata_schema():
    expires_at = datetime.now()
    token = TokenData(access_token='something', expires_at=expires_at)

    assert token.model_dump() == {
        'access_token': token.access_token,
        'expires_at': expires_at,
    }


def test_user_login_schema():
    user = UserLogin(username='carlos', password='pass123!')

    assert user.model_dump() == {
        'username': user.username,
        'password': user.password,
    }


def test_user_output_schema():
    user = UserOutput(
        username='corso',
        id=3, email='carlos@email.com',
        is_staff=False,
    )

    assert user.model_dump() == {
        'username': user.username,
        'id': user.id,
        'email': user.email,
        'is_staff': user.is_staff,
    }


def test_form_change_password_schema():
    form = FormChangePassword(
        password='pass123!',
        confirm_password='pass123!',
        new_password='Pass1234#'
    )

    assert form.model_dump() == {
        'password': 'pass123!',
        'confirm_password': 'pass123!',
        'new_password': 'Pass1234#'
    }


def test_form_change_password_invalid_passwords_schema():
    with pytest.raises(ValueError):
        form = FormChangePassword(
            password='pass123!',
            confirm_password='pas123!',
            new_password='Pass1234#'
        )


def test_form_change_email_schema():
    form = FormChangeEmail(
        password='pass123!',
        confirm_password='pass123!',
        new_email='foo@bar.com'
    )

    assert form.model_dump() == {
        'password': 'pass123!',
        'confirm_password': 'pass123!',
        'new_email': 'foo@bar.com'
    }
