import hashlib

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.TextField()
    email = models.EmailField(unique=True)

    def get_name(self):
        return str(self.name) + ' ' + str(self.surname)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()  # Хэширует пароль с использованием SHA-256

    def verify_password(self, password):
        return self.hash_password(password) == self.password

    class Meta:
        verbose_name_plural = 'users'
        db_table = 'users'
