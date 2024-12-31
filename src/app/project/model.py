from tortoise import fields

from src.base.model import BaseModel


class ProjectModel(BaseModel):
    owner = fields.ForeignKeyField(
        "models.UserModel", related_name="projects", on_delete=fields.CASCADE
    )

    name = fields.CharField(max_length=50)
    description = fields.CharField(max_length=100)

    class Meta:
        table = "projects"
