from django.db import models

# Create your models here.

import uuid

from multiselectfield import MultiSelectField

from embed_video.fields import EmbedVideoField


class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)

    updated_at =models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class IndustryChoices(models.TextChoices):
    MOLLYWOOD ='Mollywood','Mollywood'

    KOLLYWOOD ='Kollywood','Kollywood'

    HOLLYWOOD ='Hollywood','Hollywood'

    TOLLYWOOD ='Tollywood','Tollywood'

class CertificationChoices(models.TextChoices):
   
   A = 'A','A'

   UA = 'U/A','U/A'

   U = 'U','U'

   SC = 'SC','SC'

class GenereChoices(models.TextChoices):

    ACTION = 'Action','Action'

    ROMANTIC = 'Romantic','Romantic'

    THRILLER = 'Thriller','Thriller'

    COMEDY = 'Comedy','Comedy'   

    HORROR = 'Horror','Horror'

class ArtistChoices(models.TextChoices):   

    MOHANLAL = 'Mohan Lal','Mohan Lal'

    MAMMOOTTY = 'Mammooty','Mammooty'

    NIVINPAULY = 'Nivin Pauly','Nivin Pauly'

class LanguageChoices(models.TextChoices):

    MALAYALAM = 'Malayalam','Malayalam'

    ENGLISH = 'English','English'

    HINDI = 'Hindi','Hindi'

    TAMIL = 'Tamil','Tamil'
    
    TELUGU = 'Telegu','Telegu'

    KANNADA = 'Kannada','Kannada'

class Industry(BaseClass):

    name = models.CharField(max_length=50)

    class Meta :

        verbose_name = 'Industries'

        verbose_name_plural = 'Indusrties'

    def __str__(self):

        return f'{self.name}'  
    
class Genere(BaseClass):

    name = models.CharField(max_length=50)

    class Meta :

        verbose_name = 'Genere'

        verbose_name_plural = 'Genere'

    def __str__(self):

        return f'{self.name}'

      

class Artist(BaseClass):

    name = models.CharField(max_length=50) 

    dob = models.DateField()

    description = models.TextField()

    class Meta :

        verbose_name = 'Artist'

        verbose_name_plural = 'Artist'

    def __str__(self):

        return f'{self.name}'

class Languages(BaseClass):

    name = models.CharField(max_length=50)

    class Meta :

        verbose_name = 'Languages'

        verbose_name_plural = 'Languages'

    def __str__(self):

        return f'{self.name}'




class Movie(BaseClass):

    name = models.CharField(max_length=50)

    photo = models.ImageField(upload_to='movies/banner-images')

    description = models.TextField()

    release_date =models.DateField()

    industry = models.ForeignKey('Industry',on_delete=models.CASCADE)

    runtime = models.TimeField()

    certification = models.CharField(max_length=5,choices=CertificationChoices.choices)

    genere = models.ManyToManyField('Genere')

    artists = models.ManyToManyField('Artist')

    video = EmbedVideoField()

    tags = models.TextField()

    # languages = MultiSelectField(choices=LanguageChoices.choices)

    languages = models.ManyToManyField('Languages')

    class Meta :

        verbose_name = 'Movies'

        verbose_name_plural = 'Movies'

    def __str__(self):

        return f'{self.name}'