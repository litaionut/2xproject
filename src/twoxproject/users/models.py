from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Step(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    step_title = models.CharField("Method title", max_length=200)
    step_description = models.CharField("Method description", max_length=1000)
    pub_date = models.DateTimeField("date published", null=True, blank=True)
    upvotes = models.ManyToManyField(User, related_name='upvoted_steps')
    unit_number = models.FloatField("Unit Number", default=0)

    def total_upvotes(self):
        return self.upvotes.count()
       
    def __str__(self):
        return self.step_title
    
class Choice(models.Model):
    step = models.ForeignKey(Step, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField("User votes for the step",default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User,null = True, on_delete=models.CASCADE)
    total_unit_number = models.FloatField("Unit Number", default=0)
    level = models.IntegerField("Level of the user",default = 0)

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        levels = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
        ]
        units_required = [
            1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
            1024, 2048, 4096, 8192, 16384, 32768,
            65536, 131072, 262144, 524288, 1048576
        ]
        for i, units in enumerate(units_required):
            if self.total_unit_number >= units:
                self.level = levels[i]
            else:
                break
        super().save(*args, **kwargs)
    