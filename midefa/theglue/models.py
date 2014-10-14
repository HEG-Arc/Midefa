from django.db import models
from django.utils.translation import ugettext_lazy as _
from midefa.settings import TIME_ZONE


class Project(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50, help_text=_("The project's name"))
    trello_api_key = models.CharField(verbose_name=_("trello's api key"), max_length=200, help_text=_("The Trello developer API key"))
    trello_api_secret = models.CharField(verbose_name=_("trello's secret key"), max_length=200, help_text=_("The Trello secret key"))
    trello_token = models.CharField(verbose_name=_("trello's user token"), max_length=200, help_text=_("The Trello token for the authorized user"))
    trello_user = models.CharField(verbose_name=_("trello's user"), max_length=50, help_text=_("The Trello authorized user"))
    board = models.OneToOneField('TrelloBoard', verbose_name=_('board'), blank=True, null=True, help_text=_("The Trello board used in this project"))
    sprint_name = models.CharField(verbose_name=_("sprint name"), max_length=50, help_text=_("String used to concatenate the sprint name"))
    sprint_counter = models.IntegerField(verbose_name=_("sprint counter"), default=0, help_text=_("The counter used to increment sprint number"))

    class Meta:
        verbose_name = _('midefa project')
        verbose_name_plural = _('midefa projects')
        ordering = ['name']

    def __str__(self):
        return "%s" % (self.name,)


class Sprint(models.Model):
    project = models.ForeignKey('Project', verbose_name=_('project'), related_name=_('sprints'), help_text=_("Project the sprint belongs to"))
    sprint_number = models.IntegerField(verbose_name=_("sprint number"), default=0, help_text=_("The number of the sprint (incremented with project.sprint_counter"))
    sprint_date = models.DateTimeField(verbose_name=_("sprint date"), blank=True, null=True, help_text=_("The date of the sprint"))
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


class TrelloBoard(models.Model):
    project_origin = models.ForeignKey('Project', verbose_name=_('project'), related_name=_('boards'), help_text=_("Project the board belongs to"))
    board_id = models.CharField(verbose_name=_("board id"), max_length=100, help_text=_("The Trello board id"))
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("The Trello board name"))
    short_url = models.URLField(verbose_name=_("short url"), max_length=200, blank=True, null=True, help_text=_("The Trello board short url"))
    closed = models.BooleanField(verbose_name=_("closed"), default=False, help_text=_("The status of the Trello board"))

    class Meta:
        verbose_name = _('Trello board')
        verbose_name_plural = _('Trello boards')
        ordering = ['name']

    def __str__(self):
        return "%s" % (self.name,)


class TrelloList(models.Model):
    trello_board = models.ForeignKey('TrelloBoard', verbose_name=_('board'), related_name=_('lists'), help_text=_("Board the list belongs to"))
    list_id = models.CharField(verbose_name=_("list id"), primary_key=True, max_length=100, help_text=_("The Trello list id"))
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("The Trello list name"))
    closed = models.BooleanField(verbose_name=_("closed"), default=False, help_text=_("The status of the Trello list"))
    pos = models.IntegerField(verbose_name=_("position"), default=0, help_text=_("The position of the Trello list"))
    watch = models.BooleanField(verbose_name=_("watch"), default=False, help_text=_("Watch for card updates in this list"))

    class Meta:
        verbose_name = _('Trello list')
        verbose_name_plural = _('Trello lists')
        ordering = ['pos']

    def __str__(self):
        return "%s/%s" % (self.trello_board.name, self.name,)


class TrelloCard(models.Model):
    trello_list = models.ForeignKey('TrelloList', verbose_name=_('list'), related_name=_('cards'), help_text=_("List the card belongs to"))
    card_id = models.CharField(verbose_name=_("card id"), primary_key=True, max_length=100, help_text=_("The Trello card id"))
    description = models.TextField(verbose_name=_("description"), blank=True, help_text=_("The Trello card description"))
    id_short = models.IntegerField(verbose_name=_("short id"), default=0, max_length=8, help_text=_("The Trello card short id"))
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("The Trello card name"))
    short_url = models.URLField(verbose_name=_("short url"), max_length=200, blank=True, null=True, help_text=_("The Trello card short url"))
    last_activity = models.DateTimeField(verbose_name=_("last activity"), auto_now_add=True, help_text=_("Timestamp of the last change on Trello"))

    class Meta:
        verbose_name = _('Trello card')
        verbose_name_plural = _('Trello cards')
        ordering = ['id_short']

    def recent_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        from pytz import timezone
        if self.last_activity > datetime.datetime.now(timezone(TIME_ZONE))-datetime.timedelta(days=7):
            return True
        else:
            return False

    def __str__(self):
        return "[#%s] %s" % (self.id_short, self.name,)


class TrelloMember(models.Model):
    member_id = models.CharField(verbose_name=_("member id"), primary_key=True, max_length=100, help_text=_("The Trello member id"))
    full_name = models.CharField(verbose_name=_("full name"), max_length=100, help_text=_("The Trello full name"))
    username = models.CharField(verbose_name=_("username"), max_length=100, help_text=_("The Trello username"))

    class Meta:
        verbose_name = _('Trello member')
        verbose_name_plural = _('Trello members')
        ordering = ['full_name']

    def __str__(self):
        return "%s" % (self.full_name,)


class TrelloCheckList(models.Model):
    trello_card = models.ForeignKey('TrelloCard', verbose_name=_('card'), related_name=_('check lists'), help_text=_("Card the check list belongs to"))
    check_list_id = models.CharField(verbose_name=_("check list id"), primary_key=True, max_length=100, help_text=_("The Trello check list id"))
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("The Trello check list name"))

    class Meta:
        verbose_name = _('Trello check list')
        verbose_name_plural = _('Trello check lists')
        ordering = ['check_list_id']

    def __str__(self):
        return "[#%s] %s" % (self.trello_card.id_short, self.name,)


class TrelloCheckListItem(models.Model):
    OPEN = 'incomplete'
    CLOSED = 'complete'
    ITEM_STATE_CHOICES = (
        (OPEN, _('Open')),
        (CLOSED, _('Done')),
    )

    trello_check_list = models.ForeignKey('TrelloCheckList', verbose_name=_('check list'), related_name=_('items'), help_text=_("Check list the item belongs to"))
    item_id = models.CharField(verbose_name=_("item id"), primary_key=True, max_length=100, help_text=_("The Trello item id"))
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("The Trello item name"))
    state = models.CharField(verbose_name=_("state"), max_length=20, choices=ITEM_STATE_CHOICES, default=OPEN)

    class Meta:
        verbose_name = _('Trello check list item')
        verbose_name_plural = _('Trello check list items')
        ordering = ['name']

    def __str__(self):
        return "%s (%s)" % (self.name, self.state,)
