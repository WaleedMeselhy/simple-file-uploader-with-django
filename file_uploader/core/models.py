from django.db import models


class File(models.Model):

    name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=200)

    class Meta:
        db_table = "file"
