from django.db import models
from django.utils.translation import ugettext_lazy as _
from midefa.settings import TIME_ZONE
import datetime
from pytz import timezone

from theglue.models import Project


class Sprint(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('project'), related_name=_('sprints'), help_text=_("Project the sprint belongs to"))
    sprint_number = models.IntegerField(verbose_name=_("sprint number"), default=0, help_text=_("The number of the sprint (incremented with project.sprint_counter"))
    start_date = models.DateTimeField(verbose_name=_("sprint start date"), blank=True, null=True, help_text=_("The start date of the sprint"))
    due_date = models.DateTimeField(verbose_name=_("sprint due date"), blank=True, null=True, help_text=_("The due date of the sprint"))

    class Meta:
        verbose_name = _('project sprint')
        verbose_name_plural = _('project sprints')
        ordering = ['sprint_number']

    def save(self, *args, **kwargs):
        if not self.sprint_number:
            self.sprint_number = self.project.sprint_counter
            self.project.sprint_counter += 1
            self.project.save()
        super(Sprint, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (self.project.sprint_name, self.sprint_number,)


class SprintPlanningMeeting(models.Model):
    pass