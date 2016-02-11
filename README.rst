==========================================================
``django.contrib.admin.options.ModelAdmin.get_urls`` issue
==========================================================

tl;dr:
======

* checkout the repo
* run `tox`
* see the code :)

Context
=======

I would like to hang off sub-urls below admin change_form
urls, e.g.: ``/admin/myapp/mymodel/<pk>/<name>/`` for custom
views and would like to pass in kwargs to the view based on the
url matcher (``kwargs`` are "safer" tham just ``args``).

However, currently I can't do that due to the below two issues:
greedy admin url matcher and not using kwargs

Greedy matcher
--------------

``django.contrib.admin.options.ModelAdmin.get_urls``
currently is a greedy matcher as per below::

    url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
    url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
    url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),

These would eat up my more specific url matchers in the admin if I add them
in my admin after the base admin's urlpatterns.

**A solution**: Changing them to more specific matching, like::


    url(r'^([^/]+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
    url(r'^[^/]+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
    url(r'^[^/]+)/$', wrap(self.change_view), name='%s_%s_change' % info),


The repo has two tests for this, one documenting the current sitaution (HTTP 404
due to eager matching) and one documenting the desired behavior.


Not using named arguments in the urlpatterns
--------------------------------------------

``django.contrib.admin.options.ModelAdmin.get_urls`` currently uses ``args`` matching,
but when extending it one could have multiple arguments coming from the url, and thus
using named arguments in the regexp would be better IMO (even the `documentation`_ uses
named arguments!), i.e.:::

    url(r'^(?<pk>[^/]+)/$', wrap(self.change_view), name='%s_%s_change' % info),


.. _documentation: https://docs.djangoproject.com/en/1.8/topics/http/urls/#passing-extra-options-to-view-functions

