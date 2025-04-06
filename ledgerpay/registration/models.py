from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class BusinessOwner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Hash the password before saving it to the database
        if self.password and len(self.password) > 50:
            # If the password is already hashed, don't hash it again
            pass
        else:
            self.password = make_password(self.password)
        super(BusinessOwner, self).save(*args, **kwargs)

    def check_password(self, password):
        # Check the given password against the stored hash
        return check_password(password, self.password)
