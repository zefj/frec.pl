from django.db import models
from django.template.defaultfilters import slugify

from ckeditor_uploader.fields import RichTextUploadingField

class Tag(models.Model):
    name = models.CharField('Tag name', max_length = 15)

    def __unicode__(self):
        return self.name

class Project(models.Model):

    title = models.CharField('Title', max_length = 128)
    text = models.TextField()
    github = models.URLField(blank = True)

    def __unicode__(self):
        return self.title    

class Post(models.Model):
    title = models.CharField('Title', max_length = 128)
    pub_date = models.DateField(blank = True, null = True, verbose_name="Publication date") 
    text = RichTextUploadingField()
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField()
    project_relation = models.ForeignKey(Project, blank = True, null = True, verbose_name='Related to project', related_name='related_posts')

    def __unicode__(self):
        return self.title

    def get_tags(self):
        return ", ".join([t.name for t in self.tags.all()])

    def get_tags_list(self):
        return [t.name for t in self.tags.all()]       

    def save(self, *args, **kwargs):
        import datetime

        now = datetime.datetime.now()

        if str(self.pub_date) > now.strftime("%Y-%m-%d"):
            self.visible = False

        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

class CVManager(models.Manager):

    def get_object_or_none(self, *args, **kwargs):
        try: 
            return CV.objects.get(**kwargs)
        except:
            return None


class CV(models.Model):
    POLISH = 'PL'
    ENGLISH = 'EN'

    CV_CHOICES = (
        (POLISH, 'Polish'),
        (ENGLISH, 'English'),
    )

    language = models.CharField('Language', max_length = 7, choices = CV_CHOICES)
    cv = models.FileField()
    upload_date = models.DateField(auto_now=True)
    objects = CVManager()

    def __unicode__(self):
        return self.language

    class Meta:
        verbose_name_plural = "CVs"          

class SingletonModel(models.Model):
    """Singleton Django Model
    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.
    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.

    Useful for things like system-wide user-editable settings.

    Source: https://gist.github.com/senko/5028413
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)


class About(SingletonModel):
    
    text = RichTextUploadingField()

    def __unicode__(self):
        return 'About text'

    class Meta:
        verbose_name_plural = "About"   

