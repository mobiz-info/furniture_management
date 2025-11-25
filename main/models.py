import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey(
        "auth.User", blank=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True, null=True,
                                related_name="updater_%(class)s_objects", on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Processing_Log(models.Model):
    created_by=models.CharField(max_length=40,blank=True)
    created_date=models.DateField(auto_now=True,blank=True,null=True)
    description=models.CharField(null=True,max_length=1024)

    class Meta:
        ordering=('-created_date',)

    def __str__(self):
        return f"Processing Logb - {self.created_date}"