from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=64,primary_key=True, default="Anonymous")
    def __str__(self):
        return str(self.id)

class Project(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    def __str__(self):
        return str(self.name)


class Token(models.Model):
    token = models.CharField(max_length=64,primary_key=True)
    user = models.ForeignKey("User",related_name="token")
    project = models.ForeignKey("Project",related_name="token")
    def __str__(self):
        return str(self.token)

class Pixel(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    color = models.IntegerField(default=0)
    project = models.ForeignKey("Project",related_name="pixel")
    finuser = models.ForeignKey("User",related_name="pixel",null=True,blank=True)
    updtime = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together =  (("project","x", "y"),)
    def __str__(self):
        return str(self.project.name+" ("+str(self.x)+","+str(self.y)+"):"+str(self.color))