from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext as _

from controlnext.models import GrowerInfo

from lizard_ui.views import UiView


class DemoMainView(UiView):
    template_name = 'controlnext_demo/main.html'
    page_title = _('ControlNEXT demo')

    def get_context_data(self, *args, **kwargs):
        context = super(DemoMainView, self).get_context_data(*args, **kwargs)
        try:
            demo_grower = GrowerInfo.objects.get(name__exact='Demo')
        except ObjectDoesNotExist:
            raise Http404
        else:
            # needed for view.grower access in template
            self.grower = demo_grower
        return context
