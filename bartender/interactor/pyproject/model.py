from pydantic import BaseModel


class Project(BaseModel):
    dependencies: list[str]


class FileModel(BaseModel):
    project: Project
