from django.db import models
from main.models import BaseModel
from main.functions import get_auto_id
from main.middlewares import RequestMiddleware
import uuid

class School(BaseModel):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.creator:
            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request

            if self._state.adding:
                # auto_id will be inherited from BaseModel
                self.creator = request.user
                self.updater = request.user

        super(School, self).save(*args, **kwargs)

    class Meta:
        db_table = 'school'
        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __str__(self):
        return self.name

    
class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    student_class = models.CharField(max_length=50 , blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    school_name = models.ForeignKey(School, on_delete=models.CASCADE,)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    class Meta:
        db_table = 'user_profile'
        verbose_name ='User Profile'
        verbose_name_plural ='User Profiles'

    def __str__(self):
        return self.name
    
