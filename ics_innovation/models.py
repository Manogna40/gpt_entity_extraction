from django.db import models

class EntityExtractorV1(models.Model):
    id = models.AutoField(primary_key=True)
    filepath = models.CharField(null=False, max_length=100)
    entities = models.CharField(null=False, max_length=1000)
    media = models.FileField(null=False, blank=True, upload_to="files")
    extracted_text = models.TextField(null=False)
    staticpath = models.CharField(null=True, max_length=100)
    category = models.CharField(null=True, max_length=100)


    def __str__(self) -> str:
        return super().__str__()
