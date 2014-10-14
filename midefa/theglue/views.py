from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from .models import Project, TrelloBoard
from .utils import fetch_boards, fetch_lists, fetch_all_cards


class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    model = Project


class ProjectFetchBoards(TemplateView):

    template_name = "theglue/project_fetch_boards.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectFetchBoards, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=kwargs['pk'])
        context['object'] = project
        boards = fetch_boards(project)
        context['object_list'] = boards
        return context


class ProjectFetchLists(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        fetch_lists(project)
        return reverse('project_detail', kwargs={'pk': project.id})


class ProjectFetchAllCards(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        fetch_all_cards(project)
        return reverse('project_detail', kwargs={'pk': project.id})


class ProjectLinkBoard(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        board = get_object_or_404(TrelloBoard, pk=kwargs['board'])
        project.board = board
        project.save()
        return reverse('project_detail', kwargs={'pk': project.id})
        #return super(ProjectLinkBoard, self).get_redirect_url(*args, **kwargs)