from abc import ABCMeta
from django.shortcuts import resolve_url as r
from django.test import TestCase
from core.models import User
from core.functions import (register_new_student, register_new_teacher,
                            register_new_company, register_new_admin)
from django.contrib.auth import get_user_model


class CreateTestUser(metaclass=ABCMeta):
    login_url = 'core:login'

    def create_user_student(self):
        username = 'estudante@fatec.sp.gov.br'
        password = '123mudar'
        register_new_student(username, password)
        data = {'username': username,
                'password': password, }
        return data

    def create_user_student_not_active(self):
        username = 'estudante_nao_ativo@fatec.sp.gov.br'
        password = '123mudar'
        register_new_student(username, password)
        User = get_user_model()
        usuario = User.objects.get(email=username)
        usuario.is_active = False
        usuario.save()
        data = {'username': username,
                'password': password, }
        return data

    def create_user_teacher(self):
        username = 'professor@fatec.sp.gov.br'
        password = '321mudar'
        register_new_teacher(username, password)
        data = {'username': username,
                'password': password, }
        return data

    def create_user_trainee_coordinator(self):
        username = 'orlando@fatec.sp.gov.br'
        password = '321mudar'
        register_new_teacher(username, password)
        user = User.objects.all()[0]
        user.is_trainee_coordinator = True
        user.save()
        data = {'username': username,
                'password': password, }
        return data

    def create_user_company(self):
        username = 'empresa@gmail.com'
        password = '123mudar'
        register_new_company(username, password)
        data = {'username': username,
                'password': password, }
        return data

    def create_user_admin(self):
        username = 'admin@admin.com'
        password = '123mudar'
        register_new_admin(username, password)
        data = {'username': username,
                'password': password, }
        return data


class coreGetIndex(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:home'))
        self.resp2 = self.client.get(r('core:home'), follow=True)

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetLoginOk(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:login'))

    def test_302_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'base.html')
        self.assertTemplateUsed(self.resp, 'login.html')


class corePostLoginOK(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.resp2 = self.client.post(r('core:login'), data, follow=True)

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'index.html')


class corePostLoginFail(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        data['password'] = 'senha_errada'
        data_not_active_user = self.create_user_student_not_active()
        self.resp = self.client.post(r(self.login_url), data)
        self.resp2 = self.client.post(r(self.login_url), data, follow=True)
        self.resp3 = self.client.post(
            r(self.login_url), data_not_active_user, follow=True)

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response_1(self):
        self.assertEqual(200, self.resp2.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp3.status_code)

    def test_template_used_1(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_template_used_2(self):
        self.assertTemplateUsed(self.resp3, 'base.html')
        self.assertTemplateUsed(self.resp3, 'login.html')


class coreGetIndexAlunoFail(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:core_index_aluno'))
        self.resp2 = self.client.get(r('core:core_index_aluno'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAlunoFail_access_denied(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r('core:core_index_aluno'))
        self.resp2 = self.client.get(r('core:core_index_aluno'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'index.html')

    def test_302_response_1(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAlunoOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r('core:core_index_aluno'))
        self.resp2 = self.client.get(r('core:core_index_aluno'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'aluno_sidebar.html')
        self.assertTemplateUsed(self.resp2, 'aluno_topbar.html')
        self.assertTemplateUsed(self.resp2, 'aluno_index.html')

    def test_200_response_1(self):
        self.assertEqual(200, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexProfessorFail(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:core_index_professor'))
        self.resp2 = self.client.get(
            r('core:core_index_professor'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexProfessorFail_access_denied(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r('core:core_index_professor'))
        self.resp2 = self.client.get(r('core:core_index_professor'),
                                     follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'index.html')

    def test_302_response_1(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexProfessorOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r('core:core_index_professor'))
        self.resp2 = self.client.get(
            r('core:core_index_professor'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'professor_sidebar.html')
        self.assertTemplateUsed(self.resp2, 'professor_topbar.html')
        self.assertTemplateUsed(self.resp2, 'professor_index.html')

    def test_200_response_1(self):
        self.assertEqual(200, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexEmpresaFail(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:core_index_empresa'))
        self.resp2 = self.client.get(
            r('core:core_index_empresa'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexEmpresaFail_access_denied(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r('core:core_index_empresa'))
        self.resp2 = self.client.get(r('core:core_index_empresa'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'index.html')

    def test_302_response_1(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexEmpresaOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r('core:core_index_empresa'))
        self.resp2 = self.client.get(
            r('core:core_index_empresa'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'empresa_sidebar.html')
        self.assertTemplateUsed(self.resp2, 'empresa_topbar.html')
        self.assertTemplateUsed(self.resp2, 'empresa_index.html')

    def test_200_response_1(self):
        self.assertEqual(200, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreLogout(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r('core:logout'), data)

    def test_200_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')
        self.assertTemplateUsed(self.resp, 'base.html')


class corePerfilProfessor(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r('core:perfil_professor'), data)

    def test_200_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'professor_mudar_perfil.html')
        self.assertTemplateUsed(self.resp, 'rodape.html')
