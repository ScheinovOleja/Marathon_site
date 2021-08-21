"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'Marathon_Site.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'Marathon_Site.dashboard.CustomAppIndexDashboard'
"""

try:
    # we use django.urls import as version detection as it will fail on django 1.11 and thus we are safe to use
    # gettext_lazy instead of ugettext_lazy instead
    from django.urls import reverse
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.core.urlresolvers import reverse
    from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        # self.children.append(
        #     modules.ModelList(
        #         title=u'Пользователи',
        #         models=(
        #             'django.contrib.auth.*',
        #             'personal_area.models.Users',
        #         ),
        #     ),
        # )
        self.children.append(
            modules.Group(
                title=u"Статистика",
                display="stacked",
                children=[
                    modules.ModelList(
                        title=u'Пользователи',
                        models=(
                            'django.contrib.auth.*',
                            'personal_area.models.Users',
                        ),
                    ),
                    modules.ModelList(
                        title=u'Марафоны',
                        models=(
                            'personal_area.models.Marathon',
                        ),
                    ),
                ]
            ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for Marathon_Site.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
