from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

from theglue.views import ProjectList, ProjectDetail, ProjectFetchBoards, ProjectLinkBoard, ProjectFetchLists, ProjectFetchAllCards, ProjectFetchLabels

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'midefa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^project/(?P<pk>\d+)/link/(?P<board>\d+)/$', ProjectLinkBoard.as_view(), name='project_link_board',),
    url(r'^project/(?P<pk>\d+)/fetch/boards$', ProjectFetchBoards.as_view(), name='project_fetch_boards',),
    url(r'^project/(?P<pk>\d+)/fetch/lists$', ProjectFetchLists.as_view(), name='project_fetch_lists',),
    url(r'^project/(?P<pk>\d+)/fetch/labels$', ProjectFetchLabels.as_view(), name='project_fetch_labels',),
    url(r'^project/(?P<pk>\d+)/fetch/all-cards$', ProjectFetchAllCards.as_view(), name='project_fetch_all_cards',),
    url(r'^project/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project_detail',),
    url(r'^projects/$', ProjectList.as_view(), name='projects',),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('login')}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
