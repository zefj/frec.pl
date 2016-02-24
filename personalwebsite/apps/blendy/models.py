from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group

class ApiUserGroup(models.Model):

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    APIKey = models.CharField('Key', blank = True, null = True, max_length = 30)

    def __unicode__(self):
        return self.group.name

    class Meta:
        verbose_name_plural = "API user groups"

    def save(self, *args, **kwargs):
        """
        Generates keys on save.
        """
        import random, string

        if not self.APIKey:
            self.APIKey = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        super(ApiUserGroup, self).save(*args, **kwargs)

class ApiUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="apiuser")
    secret = models.CharField('Secret', blank = True, null = True, max_length = 30)
    group = models.ForeignKey(ApiUserGroup, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "API user"

    def save(self, *args, **kwargs):
        """
        Generates keys on save.
        """
        import random, string

        if not self.secret:
            self.secret = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        super(ApiUser, self).save(*args, **kwargs)

class DailyUsageLog(models.Model):

    group = models.ForeignKey(ApiUserGroup, on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)
    words_checked = models.IntegerField()


