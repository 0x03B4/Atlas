from django.urls import reverse
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from .models import Qualification, Module, Student, Lecturer
from .forms import StudentProfileForm


class QualificationModelTest(TestCase):
    def setUp(self):
        self.qualification = Qualification.objects.create(
            name="BSc in Computer Science",
            description="A foundational degree in computing.",
            duration_years=3,
            total_credits=360,
            total_modules=24,
            format='Contact'
        )

    def test_qualification_creation(self):
        self.assertEqual(self.qualification.name, "BSc in Computer Science")
        self.assertEqual(self.qualification.duration_years, 3)
        self.assertEqual(str(self.qualification), "BSc in Computer Science")

    def test_semesters_property(self):
        self.assertEqual(self.qualification.semesters, 6)


class CoreViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser@example.com', email='testuser@example.com', password='testpassword123')
        self.qualification = Qualification.objects.create(
            name="BSc in Data Science",
            description="A degree in data.",
            duration_years=3,
            total_credits=360,
            total_modules=24
        )
        self.student = Student.objects.create(
            user=self.user, 
            student_number="12345678"
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_programs_view(self):
        response = self.client.get(reverse('programs_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programs_view.html')
        self.assertContains(response, self.qualification.name)

    def test_program_detail_view(self):
        response = self.client.get(reverse('program_detail', args=[self.qualification.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'program_detail.html')
        self.assertContains(response, self.qualification.name)

    @override_settings(LOGIN_URL='student_login')
    def test_student_dashboard_unauthenticated(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        self.assertRedirects(response, f"{reverse('student_login')}?next={reverse('student_dashboard')}")

    def test_student_dashboard_incomplete_profile(self):
        self.client.login(username='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_profile'))

    def test_student_dashboard_complete_profile(self):
        self.student.qualification = self.qualification
        self.student.current_year = 1
        self.student.current_semester = 1
        self.student.save()

        self.client.login(username='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')
        self.assertIn('academic_progress', response.context)

    def test_student_signup(self):
        response = self.client.post(reverse('student_signup'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'password': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_login'))
        
        self.assertTrue(User.objects.filter(email='janedoe@example.com').exists())
        self.assertTrue(Student.objects.filter(user__email='janedoe@example.com').exists())


class StudentProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testform@example.com', email='testform@example.com', password='password')
        self.student = Student.objects.create(user=self.user, student_number='98765432')
        self.qualification = Qualification.objects.create(
            name="BCom Accounting",
            description="A degree in accounting.",
            duration_years=3,
            total_credits=360,
            total_modules=24
        )

        User.objects.create_user(username='another@example.com', email='another@example.com', password='password')

    def test_valid_form(self):
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testform@example.com',
            'qualification': self.qualification.pk,
            'current_year': 1,
            'current_semester': 2,
        }
        form = StudentProfileForm(data=form_data, instance=self.student, user=self.user)
        self.assertTrue(form.is_valid())

    def test_email_in_use(self):
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'another@example.com',
            'qualification': self.qualification.pk,
            'current_year': 1,
            'current_semester': 2,
        }
        form = StudentProfileForm(data=form_data, instance=self.student, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "This email is already in use by another account.")

    def test_form_save(self):
        form_data = {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'newemail@example.com',
            'qualification': self.qualification.pk,
            'current_year': 2,
            'current_semester': 1,
        }
        form = StudentProfileForm(data=form_data, instance=self.student, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        self.student.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, 'UpdatedFirst')
        self.assertEqual(self.user.last_name, 'UpdatedLast')
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.username, 'newemail@example.com')
        self.assertEqual(self.student.qualification, self.qualification)
        self.assertEqual(self.student.current_year, 2)
