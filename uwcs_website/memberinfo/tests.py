from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

class AuthTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.password = User.objects.make_random_password()
        self.username = "unitTester"
        self.email = "t.r.monks@gmail.com"
        u = User.objects.create_user(self.username, self.email, self.password)
        u.is_staff = True
        u.save()

    def tearDown(self):
        User.objects.get(username=self.username).delete()
    
    def testAddUser(self):
        testcase_username = 'testcase'
        testcase_password = User.objects.make_random_password()
        
        self.c.login(username=self.username, password=self.password)
        self.c.post('http://uwcs.co.uk/admin/auth/user/add/', {
            'username':testcase_username, 
            'password1':testcase_password, 
            'password2':testcase_password
        })
        #User.objects.get(username=testcase_username).delete()


    def testLogin(self):
       self.assertContains(self.c.post('/login/', {"username": self.username, "password": self.password, "next":""}, follow=True), "Logged in as")
