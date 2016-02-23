from __future__ import unicode_literals
import random, string
from django.db import models

class ApiUsers(models.Model):

    name = models.CharField('Name', max_length = 128)
    APIKey = models.CharField('Key', blank = True, null = True, max_length = 15)
    secret = models.CharField('Key', blank = True, null = True, max_length = 15)

    def __unicode__(self):
        return self.name    

    class Meta:
        verbose_name_plural = "API users"

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        if not self.APIKey:
            self.APIKey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        if not self.secret:
            self.secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))    
        super(ApiUsers, self).save(*args, **kwargs)

class DailyBill(models.Model):

    user = models.ForeignKey(ApiUsers, on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)
    words_checked = models.IntegerField()

    def __unicode__(self):
        return unicode(self.user)