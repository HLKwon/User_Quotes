from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re, bcrypt



lettersOnly = re.compile(r'^[a-zA-Z]*$')
emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class userManager(models.Manager):
    def rValidate(self, postData):
        errors = []
        flag = False

        if not postData['name']:
            errors.append('Name must not be blank.')
            flag = True
        if len(postData['name']) < 2:
            errors.append('Name must be longer than 2 characters.')
            flag = True
        if not lettersOnly.match(postData['name']):
            errors.append('Name must not contain numbers.')
            flag = True

        if not postData['alias']:
            errors.append('Alias must not be blank.')
            flag = True
        if len(postData['alias']) < 2:
            errors.append('Alias must be longer than 2 characters.')
            flag = True

        if not postData['email']:
            errors.append('Email must not be blank.')
            flag = True
        if not emailRegex.match(postData['email']):
            errors.append('Email must be valid.')
            flag = True

        if not postData['password']:
            errors.append('Password must not be blank')
            flag = True
        if len(postData['password']) < 8:
            errors.append('Password must be greater than 8 characters')
            flag = True
        if postData['password'] != postData['cPassword']:
            errors.append('Passwords must match!')
            flag = True

        if not postData['birthday']:
            errors.append("Date of Birth is blank.")
            flag = True


        if not flag:
            bday = datetime.strptime(postData['birthday'], "%Y-%m-%d")
            hashedPW = bcrypt.hashpw( postData['password'].encode(), bcrypt.gensalt() )
            user = User.objects.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                password=hashedPW,
                birthday=bday
            )
            return(flag, user)

        return (flag, errors)


    def lValidate(self, postData):

        if not postData['email']:
            return(False, "Login credentials are invalid.")

        if not emailRegex.match(postData['email']):
            return(False, "Login credentials are invalid.")


        if not postData['password']:
            return(False, "Login credentials are invalid.")

        user = User.objects.get(email=postData['email'])
        password = postData['password'].encode()
        hashed = user.password.encode()

        if bcrypt.hashpw(password, hashed) == hashed:
            return (True, user)

        return(False, "Login credentials are invalid.")





class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poked = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="poked_by")
    objects = userManager()
