"""Testcases for Interviews."""
import json

from rest_framework.test import APITestCase

from .models import CandidateTestMapping
from .factories import QuestionFactory
from .factories import TestFactory
from .models import User
from .views import UserViewSet


class UserViewSetTest(APITestCase):
    """ Test class for testing UserViewSet APIs."""

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com',
                                             password='test12345')

    def test_user_creation(self):
        """ To test user create API."""
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/user/',
                                    {'email': 'test@example.com',
                                     'password': 'test12345'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertNotEqual(response.data['password'], 'test12345')

    def test_user_get(self):
        """To test user get API."""
        TestFactory.build()
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.get('/interview/user/')
        self.assertEqual(response.status_code, 200)

    def test_user_retrieve(self):
        """To test user retrieve API."""
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/user/',
                                 {'email':'test@example.com',
                                  'password':'test12345'})
        user_id = response.data['id']
        response = self.client.get('/interview/user/%s/'%user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_type_default(self):
        """To test default user type."""
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/user/',
                             {'email': 'test@example.com',
                              'password': 'test12345'})
        user_id = response.data['id']
        response = self.client.get('/interview/user/%s/'%user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_type'], 'INTERVIEWER')

    def test_user_type_interviewer(self):
        """To test interviewer user type."""
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/user/',
                             {'email': 'test@example.com',
                              'password': 'test12345',
                              'user_type': 'INTERVIEWER'})
        user_id = response.data['id']
        response = self.client.get('/interview/user/%s/'%user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_type'], 'INTERVIEWER')

    def test_user_type_candidate_with_no_test(self):
        """To test candidate user type with no test."""
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/user/',
                             {'email': 'test@example.com',
                              'password': 'test12345',
                              'user_type': 'CANDIDATE'})
        self.assertEqual(response.status_code, 400)

    def test_user_type_candidate_with_test(self):
        """To test candidate user type with test."""
        self.client.login(email='testuser@example.com', password='test12345')
        question_object = QuestionFactory.build()
        _ = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                  'duration': 60,
                                                  'question': question_object})
        test_id = _.data['id']
        print(test_id)
        response = self.client.post('/interview/user/',
                             {'email': 'test@example.com',
                              'password': 'test12345',
                              'user_type': 'CANDIDATE', 'test_id': test_id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CandidateTestMapping.objects.count(), 1)

    def test_user_delete(self):
        """To test user delete API."""
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/user/',
                             {'email': 'test@example.com',
                              'password': 'test12345'})
        user_id = response.data['id']
        response = self.client.delete('/interview/user/%s/'%user_id)
        self.assertEqual(response.status_code, 204)


class TestViewSetTest(APITestCase):
    """Test class for testing TestViewSet APIs."""

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com',
                                             password='test12345')
        self.another_user = User.objects.create_user(
            email='testuser1@example.com', password='test12345')

    def test_test_creation(self):
        """testing create API of test."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                         'duration': 60,
                                                         'question':
                                                             question_object})
        self.assertEqual(response.status_code, 201)

    def test_test_get_owner_user(self):
        """testing get API of test."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com', password='test12345')
        _ = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                  'duration': 60,
                                                  'question': question_object})
        response = self.client.get('/interview/test/')
        self.assertEqual(response.status_code, 200)

    def test_test_retrieve_owner_user(self):
        """testing retrieval of test."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                         'duration': 60,
                                                         'question':
                                                             question_object})
        test_id = response.data['id']
        response = self.client.get('/interview/test/%s/'%test_id)
        self.assertEqual(response.data['title'], 'Dev Test')
        self.assertEqual(response.status_code, 200)

    def test_test_update_owner_user(self):
        """testing update API of test."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                         'duration': 60,
                                                         'question':
                                                             question_object})
        test_id = response.data['id']
        response = self.client.put('/interview/test/%s/'%test_id,
                                    {'title': 'Development Test',
                                     'duration': 60, 'question':
                                         question_object})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/interview/test/%s/' % test_id)
        self.assertEqual(response.data['title'], 'Development Test')
        self.assertEqual(response.status_code, 200)

    def test_test_delete_owner_user(self):
        """testing delete API of test."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com', password='test12345')
        response = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                         'duration': 60,
                                                         'question':
                                                             question_object})
        test_id = response.data['id']
        response = self.client.delete('/interview/test/%s/' % test_id)
        self.assertEqual(response.status_code, 204)

    def test_test_get_another_user(self):
        """testing get API of test using another user."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com',
                          password='test12345')
        _ = self.client.post('/interview/test/', {'title': 'Dev Test',
                                                  'duration': 60,
                                                  'question': question_object})
        self.client.login(email='testuser1@example.com',
                          password='test12345')
        response = self.client.get('/interview/test/')
        self.assertEqual(response.status_code, 200)

    def test_test_retrieve_another_user(self):
        """testing retrieval of test using another user."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com',
                          password='test12345')
        response = self.client.post('/interview/test/',
                                    {'title': 'Dev Test',
                                     'duration': 60,
                                     'question':
                                         question_object})
        test_id = response.data['id']
        self.client.login(email='testuser1@example.com',
                          password='test12345')
        response = self.client.get('/interview/test/%s/' % test_id)
        self.assertEqual(response.data['title'], 'Dev Test')
        self.assertEqual(response.status_code, 200)

    def test_test_update_another_user(self):
        """testing update API of test using another user."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com',
                          password='test12345')
        response = self.client.post('/interview/test/',
                                    {'title': 'Dev Test',
                                     'duration': 60,
                                     'question':
                                         question_object})
        test_id = response.data['id']
        self.client.login(email='testuser1@example.com',
                          password='test12345')
        response = self.client.put('/interview/test/%s/' % test_id,
                                   {'title': 'Development Test',
                                    'duration': 60, 'question':
                                        question_object})
        self.assertEqual(response.status_code, 403)

    def test_test_delete_another_user(self):
        """testing delete API of test using another user."""
        question_object = QuestionFactory.build()
        self.client.login(email='testuser@example.com',
                          password='test12345')
        response = self.client.post('/interview/test/',
                                    {'title': 'Dev Test',
                                     'duration': 60,
                                     'question':
                                         question_object})
        test_id = response.data['id']
        self.client.login(email='testuser1@example.com',
                          password='test12345')
        response = self.client.delete('/interview/test/%s/' % test_id)
        self.assertEqual(response.status_code, 403)


class QuestionViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com',
                                             password='test12345')

    def test_question_creation(self):
        self.client.login(email='testuser@example.com', password='test12345')
        with open('/home/arunv/Documents/file1.py') as fp1, \
             open('/home/arunv/Documents/file2.py') as fp2, \
             open('/home/arunv/Documents/file3.py') as fp3:
            response = self.client.post('/interview/question/',
                                    {'title': 'Dev Test', 'question_id': '1',
                                     'question_type': 'Programming',
                                     'problem_statement': fp1,
                                     'test_cases': fp2,
                                     'skeleton': fp3, 'marks': 100})
        self.assertEqual(response.status_code, 201)