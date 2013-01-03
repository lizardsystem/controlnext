from django.utils.translation import ugettext as _

from controlnext.views import MainView


class DemoMainView(MainView):
    template_name = 'controlnext_demo/main.html'
    page_title = _('ControlNEXT demo')
