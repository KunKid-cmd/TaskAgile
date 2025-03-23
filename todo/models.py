from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class TodoItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='Pending')
    image = CloudinaryField('image', blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            old = TodoItem.objects.get(pk=self.pk)
            if old.image and old.image != self.image:
                destroy(old.image.public_id)
        except TodoItem.DoesNotExist:
            pass

        super().save(*args, **kwargs)


@receiver(post_delete, sender=TodoItem)
def delete_todo_image_from_cloudinary(sender, instance, **kwargs):
    if instance.image:
        try:
            destroy(instance.image.public_id)
        except Exception as e:
            print(f"[Cloudinary] Failed to delete image: {e}")
