from import_export import resources
from .models import MenstrualCyclePrediction, Assignment, Task

class MenstrualCyclePredictionResource(resources.ModelResource):
    class Meta:
        model = MenstrualCyclePrediction

class AssignmentResource(resources.ModelResource):
    class Meta:
        model = Assignment

class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
