from django.db import models

# Create your models here.
class Packages(models.Model):
    p_id =models.AutoField(auto_created=True,primary_key=True)
    packagess_name = models.CharField(max_length=120, null=False,db_index=True)
    destination_List = models.CharField(max_length=60)
    description = models.CharField(max_length=1200)
    price =models.CharField(max_length=200)
    rating = models.CharField(max_length=120)
    image = models.ImageField(upload_to='packages_img',blank=True)
    cover_pick = models.IntegerField()
    event = models.CharField(max_length=120)
    is_featured= models.BooleanField()

    def __str__(self):
        return self.packagess_name