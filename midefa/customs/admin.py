from sitetree.admin import TreeItemAdmin, override_item_admin
from django.utils.translation import ugettext_lazy as _

# And our custom tree item admin model.


class CustomTreeItemAdmin(TreeItemAdmin):
    # That will turn a tree item representation from the default variant
    # with collapsible groupings into a flat one.
    fieldsets = (
        (_('Basic settings'), {
        'fields': ('parent', 'title', 'url',)
        }),
        (_('Access settings'), {
        'classes': ('collapse',),
        'fields': ('access_loggedin', 'access_guest', 'access_restricted', 'access_permissions', 'access_perm_type')
        }),
        (_('Display settings'), {
        'classes': ('collapse',),
        'fields': ('hidden', 'inmenu', 'inbreadcrumbs', 'insitetree')
        }),
        (_('Additional settings'), {
        'classes': ('collapse',),
        'fields': ('hint', 'css_class', 'description', 'alias', 'urlaspattern')
        }),
    )

# Now we tell the SiteTree to replace generic representations with custom.
override_item_admin(CustomTreeItemAdmin)