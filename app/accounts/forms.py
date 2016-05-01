#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional
from flask.ext.login import current_user
from flask.ext.mongoengine.wtf import model_form

from . import models

class LoginForm(Form):
    username = StringField()
    password = PasswordField()
    remember_me = BooleanField('Keep me logged in')

class RegistrationForm(Form):
    username = StringField('Username', validators=[Required(), Length(1,64), 
        Regexp('^[A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])

    def validate_username(self, field):
        if models.User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('Username already in use')

    def validate_email(self, field):
        if models.User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('Email already in registered')

class UserForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    # is_active = BooleanField('Is activie')
    # is_superuser = BooleanField('Is superuser')
    role = SelectField('Role', choices=models.ROLES)

# SuUserForm = model_form(models.User, exclude=['create_time', 'last_login', 'password_hash'])

class SuUserForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    is_superuser = BooleanField('Is superuser')
    is_email_confirmed = BooleanField('Is Email Confirmed') 
    role = SelectField('Role', choices=models.ROLES)
    display_name = StringField('Display Name', validators=[Length(1,128)])
    biography = StringField('Biograpyh')
    homepage_url = StringField('Homepage', validators=[URL(), Optional()])
    weibo = StringField('Weibo', validators=[URL(), Optional()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    twitter = StringField('Twitter', validators=[URL(), Optional()])
    github = StringField('github', validators=[URL(), Optional()])
    facebook = StringField('Facebook', validators=[URL(), Optional()])
    linkedin = StringField('Linkedin', validators=[URL(), Optional()])

# ProfileForm = model_form(models.User, exclude=['username', 'password_hash', 'create_time', 'last_login', 
#     'is_email_confirmed', 'is_superuser', 'role'])
class ProfileForm(Form):
    # email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    display_name = StringField('Display Name', validators=[Length(1,128)])
    biography = StringField('Biography')
    homepage_url = StringField('Homepage', validators=[URL(), Optional()])
    avatar_url = StringField('Avatar', validators=[URL(), Optional()])
    weibo = StringField('Weibo', validators=[URL(), Optional()])
    weixin = StringField('Weixin', validators=[Optional(), URL()])
    twitter = StringField('Twitter', validators=[URL(), Optional()])
    # github = StringField('github', validators=[URL(), Optional()])
    facebook = StringField('Facebook', validators=[URL(), Optional()])
    linkedin = StringField('Linkedin', validators=[URL(), Optional()])

class PasswordForm(Form):
    current_password = PasswordField('Current Password', validators=[Required()])
    new_password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Current password is wrong')

class PasswordForm2(Form):
    new_password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Current password is wrong')

class UsernameForm(Form):
    username = StringField('Username', validators=[Required(), Length(1,64), 
        Regexp('^[A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    password = PasswordField('Password', validators=[Required()])
    
    def validate_username(self, field):
        users = models.User.objects(username=field.data)
        if users.count() > 0 and users[0].id != current_user.id:
            raise ValidationError('Username already in use')


    def validate_email(self, field):
        users = models.User.objects.filter(email=field.data)
        if users.count() > 0 and users[0].id != current_user.id:
            raise ValidationError('Email already in registered')

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Current password is wrong')
