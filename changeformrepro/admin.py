from functools import update_wrapper
from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse
from changeformrepro.models import MyModel


class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        parent_urlpatterns = super(MyModelAdmin, self).get_urls()
        change_pattern, = (p for p in parent_urlpatterns if p.name.endswith('_change'))
        change_form_regex = change_pattern._regex
        if change_form_regex[-1] == '$':
            change_form_regex = change_form_regex[:-1]
        if change_form_regex[-1] == '/':
            change_form_regex = change_form_regex[:-1]

        extra_url_patterns = patterns(
            '',
            url(r'%s/(\S+)/' % change_form_regex,  # NOTE: I can't use kwargs here
                wrap(self.greet_view),
                name='changeformrepro_mymodel_greet'),
        )

        return parent_urlpatterns + extra_url_patterns

    def greet_view(self, request, pk, greeting):
        obj = MyModel.objects.get(pk=pk)
        return HttpResponse('%s %s' % (greeting, obj.name))


admin.site.register(MyModel, MyModelAdmin)
