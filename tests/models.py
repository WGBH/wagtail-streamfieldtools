from django.db import models

from streamfield_tools.fields import RegisteredBlockStreamField


class RegisteredBlockStreamFieldTestModel(models.Model):
    vanilla = RegisteredBlockStreamField(blank=True)
    exclude = RegisteredBlockStreamField(exclude_blocks=['heading'])
    include = RegisteredBlockStreamField(only_blocks=['heading'])
