from django.db import models


class BaseModel(models.Model):
    app_label = 'reservation_app'
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
