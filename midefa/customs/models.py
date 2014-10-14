from django.db import models
from sitetree.models import TreeItemBase, TreeBase


class MidefaTreeItem(TreeItemBase):
    """And that's a tree item model with additional `css_class` field."""
    css_class = models.CharField(verbose_name="css class", max_length=100, blank=True, default='', help_text="You can add a fontawesome class")
