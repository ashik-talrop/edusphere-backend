from django.db import models
from main.models import BaseModel
from main.middlewares import RequestMiddleware
from main.functions import get_auto_id
from django.template.defaultfilters import slugify



class Post(BaseModel):
    user = models.ForeignKey("accounts.UserProfile",on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)
    like = models.ManyToManyField("accounts.UserProfile",related_name='liked_posts',blank=True)
    saved_by = models.ManyToManyField("accounts.UserProfile", related_name='saved_posts', blank=True)
    
    class Meta:
        db_table = 'post'
        verbose_name ='Post'
        verbose_name_plural ='Posts'
        ordering = ['-date_added']

    def get_auto_id(self):
        last_auto_id = Post.objects.filter(is_deleted=False).order_by('-auto_id').first()
        if last_auto_id:
            return last_auto_id.auto_id + 1
        return 1
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.auto_id = self.get_auto_id()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.user.name}"
    

class Comment(BaseModel):
    user = models.ForeignKey("accounts.UserProfile",on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=48)


    class Meta:
        db_table = 'comment'
        verbose_name ='Comment'
        verbose_name_plural ='Comments'

    def __str__(self):
        return f"{self.comment_text} liked by {self.user.name}"
    
    def save(self, *args, **kwargs):
        if not self.auto_id:
            max_auto_id = Comment.objects.aggregate(models.Max('auto_id'))['auto_id__max'] or 0
            self.auto_id = max_auto_id + 1
        super().save(*args, **kwargs)

