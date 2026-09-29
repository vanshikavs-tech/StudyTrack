from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task


class StudyTrackTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='student1', password='password123')
        self.user2 = User.objects.create_user(username='student2', password='password123')
        self.task1 = Task.objects.create(
            user=self.user1,
            title='DSA Assignment',
            description='Binary search tree implementation',
            completed=False
        )
        self.task2 = Task.objects.create(
            user=self.user1,
            title='Math Homework',
            description='Calculus exercises',
            completed=True
        )

    def test_root_redirects_to_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_login_flow(self):
        response = self.client.post('/login/', {
            'username': 'student1',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)

    def test_dashboard_displays_user_tasks_and_statistics(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, student1!')
        self.assertContains(response, 'Total Tasks')
        self.assertEqual(response.context['total_tasks'], 2)
        self.assertEqual(response.context['completed_tasks'], 1)
        self.assertContains(response, 'DSA Assignment')
        self.assertContains(response, 'Math Homework')

    def test_add_task(self):
        self.client.login(username='student1', password='password123')
        response = self.client.post('/tasks/add/', {
            'title': 'New Physics Lab',
            'description': 'Experiment on optics'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')
        
        # Verify task is created and assigned to student1
        task = Task.objects.get(title='New Physics Lab')
        self.assertEqual(task.user, self.user1)
        self.assertFalse(task.completed)

    def test_complete_task(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(f'/tasks/{self.task1.id}/complete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

    def test_delete_task_via_post(self):
        self.client.login(username='student1', password='password123')
        response = self.client.post(f'/tasks/{self.task1.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_user_cannot_modify_or_delete_another_user_task(self):
        # User 2 logs in and attempts to complete or delete user1's task
        self.client.login(username='student2', password='password123')

        # Attempt to complete User 1's task
        response_complete = self.client.get(f'/tasks/{self.task1.id}/complete/')
        self.assertEqual(response_complete.status_code, 404)

        # Attempt to delete User 1's task
        response_delete = self.client.post(f'/tasks/{self.task1.id}/delete/')
        self.assertEqual(response_delete.status_code, 404)

        # Task 1 must remain intact and incomplete
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.completed)
        self.assertTrue(Task.objects.filter(id=self.task1.id).exists())

    def test_user_isolation_on_dashboard(self):
        # User 2 dashboard should show 0 tasks
        self.client.login(username='student2', password='password123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_tasks'], 0)
        self.assertEqual(response.context['completed_tasks'], 0)
        self.assertNotContains(response, 'DSA Assignment')

    def test_logout_flow(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        # Dashboard should now redirect to login
        dashboard_response = self.client.get('/dashboard/')
        self.assertEqual(dashboard_response.status_code, 302)
        self.assertIn('/login/', dashboard_response.url)
