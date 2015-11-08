from django.db import models
from django.template.defaultfilters import slugify

from ckeditor_uploader.fields import RichTextUploadingField

class Tag(models.Model):
    name = models.CharField('Tag name', max_length = 15)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('Title', max_length = 128)
    pub_date = models.DateField(blank = True, verbose_name="Publication date") # blank tru, do sprobowania: jesli bez daty, to nie publiszt
    text = RichTextUploadingField()
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField()
    visible = models.BooleanField('Published', default = True)

    def __unicode__(self):
        return self.title

    def get_tags(self):
        return ", ".join([t.name for t in self.tags.all()])

    def save(self, *args, **kwargs):
        import datetime

        now = datetime.datetime.now()

        if str(self.pub_date) > now.strftime("%Y-%m-%d"):
            self.visible = False


        if not self.id:
            self.slug = slugify(self.title)



        super(Post, self).save(*args, **kwargs)