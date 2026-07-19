from django.test import TestCase
from api.models import Task


class TaskModelTest(TestCase):
    def test_task_creation(self):
        """Простой тест: создаём задачу и проверяем строковое представление."""
        task = Task.objects.create(
            title='Test Task',
            description='Test description'
        )
        self.assertEqual(str(task), 'Test Task')
