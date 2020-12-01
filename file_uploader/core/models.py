from django.db import models


class File(models.Model):

    name = models.TextField(max_length=1000)
    file_path = models.TextField(max_length=1000)

    class Meta:
        db_table = "file"
