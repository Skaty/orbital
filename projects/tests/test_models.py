from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from projects.models import Project, ProjectGroup


class ProjectTestCase(TestCase):
    def test_create_project(self):
        """
        Tests if a project can be created.

        Coverage:
            - Creation of Project model instance
            - Persistence of Project model instance in DB
        """
        mock_facilitator = User.objects.create_user('facilitator')
        parameters = {
            'name': 'Test Project'
        }

        project = Project.objects.create(**parameters)
        retrieved_project = Project.objects.get(pk=project.pk)

        project.facilitators.add(mock_facilitator)

        for key, value in parameters.items():
            self.assertEqual(value, getattr(retrieved_project, key),
                             "{key} attribute of instance is {value} in DB".format(key=key, value=value))

        self.assertIn(retrieved_project, mock_facilitator.project_set.all(),
                      "Assert the existence of a reverse relationship from User to Project")

    def test_is_active_method(self):
        """
        Tests the behaviour of the is_active model method.

        Coverage:
            - Checks if is_active has been declared
            - Output of is_active is as expected
        """
        parameters = {
            'name': 'Test Project',
            'ends_on': timezone.now() - timedelta(days=1),
        }
        expired_project = Project.objects.create(**parameters)

        self.assertFalse(expired_project.is_active(),
                         "An expired/ended project is inactive")

        parameters['ends_on'] = timezone.now() + timedelta(days=1)
        active_project = Project.objects.create(**parameters)

        self.assertTrue(active_project.is_active(),
                        "A project with ending date > now is active")

    def test_string_representation(self):
        """
        Tests the string representation of Project model instance
        Coverage:
            - String representation of Project model instance
        """
        parameters = {
            'name': 'Test Project 123',
        }
        project = Project.objects.create(**parameters)

        self.assertEqual(project.name, str(project),
                         "String representation of name is equal to the instance's name attribute")

class ProjectGroupTestCase(TestCase):
    def test_create_group(self):
        """
        Tests if a group can be created.

        Coverage:
            - Creation of ProjectGroup model instance
            - Persistence of ProjectGroup model instance in DB
        """
        mock_member = User.objects.create_user('group_member')
        mock_project = Project.objects.create(name="Test")

        parameters = {
            'name': 'Test Group',
            'project': mock_project,
        }

        project_group = ProjectGroup.objects.create(**parameters)
        retrieved_project_group = ProjectGroup.objects.get(pk=project_group.pk)

        project_group.members.add(mock_member)

        for key, value in parameters.items():
            self.assertEqual(value, getattr(retrieved_project_group, key),
                             "{key} attribute of instance {value} in DB".format(key=key, value=value))

        self.assertIn(retrieved_project_group, mock_project.projectgroup_set.all(),
                      "Assert the existence of a reverse relationship from Project to ProjectGroup")

        self.assertIn(retrieved_project_group, mock_member.projectgroup_set.all(),
                      "Assert the existence of a reverse relationship from User to ProjectGroup")

    def test_string_representation(self):
        """
        Tests the string representation of ProjectGroup model instance
        Coverage:
            - String representation of ProjectGroup model instance
        """
        parameters = {
            'name': 'Test Group',
        }
        project_group = Project.objects.create(**parameters)

        self.assertEqual(project_group.name, str(project_group),
                         "String representation of name is equal to the instance's name attribute")
