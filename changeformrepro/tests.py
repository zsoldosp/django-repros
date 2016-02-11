import re
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, clear_url_caches
from django.test.testcases import TransactionTestCase
from django.test.utils import override_settings
from changeformrepro.models import MyModel
from changeformrepro.admin import MyModelAdmin


class MyModelAdminTestCase(TransactionTestCase):
    def setUp(self):
        super(MyModelAdminTestCase, self).setUp()
        self.mymodel = MyModel.objects.create(name='world')

        self.admin = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.admin.set_password('admin')
        self.admin.save()

        self.assertTrue(self.client.login(username='admin', password='admin'))

        self.url = reverse('admin:changeformrepro_mymodel_greet', args=[self.mymodel.pk, 'hello'])

    @override_settings(DEBUG=True)
    def test_the_problematic_current_behavior(self):
        r = self.client.get(self.url)
        self.assertEqual(404, r.status_code, (self.url, r.status_code, r.content))  # sub url
        match = re.search('my model object with primary key u&#39;%s/hello&#39; does not exist.' % self.mymodel.pk, r.content)
        self.assertIsNotNone(match)

    def test_the_desired_behavior(self):
        """
        could be achived by changing the matcher in
        ``django.contrib.admin.options.ModelAdmin.get_urls``
        from::

            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),

        to::

            url(r'^([^/]+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^[^/]+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^[^/]+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        """
        MyModelAdmin.parent_first = False
        r = self.client.get(self.url)
        self.assertEqual(200, r.status_code, (self.url, r.status_code, r.content))  # sub url404
        self.assertEqual('hello world', r.content)
