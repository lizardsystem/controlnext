import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext as _

from controlnext.models import GrowerInfo, is_valid_crop_type, Basin

from lizard_ui.views import UiView

logger = logging.getLogger(__name__)


class DemoMainView(UiView):
    template_name = 'controlnext_demo/main.html'
    page_title = _('ControlNEXT demo')

    def get_context_data(self, *args, **kwargs):
        context = super(DemoMainView, self).get_context_data(*args, **kwargs)
        try:
            self.basin = Basin.objects.get(name__iexact='demo')
        except ObjectDoesNotExist:
            raise Http404
        # add crop type if given
        crop = self.request.GET.get('crop')  # None if none given
        if crop and is_valid_crop_type(crop):
            # also need a <crop>.jpg in the static/ directory
            self.crop_type = crop.lower()
        elif crop:
            logger.error("Invalid crop type: %s" % crop)
        return context
