import uuid

from django.contrib.auth.models import User
from django.db import models


class BaseTimestampModel(models.Model):
    """
    An abstract base class model that provides self-updating 'created_at' 
    and 'updated_at' fields along with 'created_by' and 'updated_by' fields.
    """
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.uid}>'
    
    def save(self, *args, **kwargs):
        # Check if 'user' is in kwargs and remove it for super().save()
        user = kwargs.pop('user', None)  # Remove 'user' from kwargs

        if user and not self.pk:  # Only set created_by if it's a new instance
            self.created_by = user
        if user:  # Always set updated_by on save
            self.updated_by = user
            
        # Call the parent class's save method
        super().save(*args, **kwargs)