from django.core.management.base import BaseCommand, CommandError

from controlnext.models import Basin
from controlnext.view_helpers import update_current_fill


class Command(BaseCommand):
    """Management command for updating fill values for all basins."""
    help = 'Updates all basins with the most current fill values.'

    def handle(self, **options):
        basins = Basin.objects.all()
        for basin in basins:
            orig_fill = basin.current_fill
            try:
                new_fill_value = update_current_fill(basin)
            # catch broad exception, because of fews call
            except Exception, info:
                raise CommandError("Error updating fill value for basin "
                                   "'%s', info: %s" % (basin, info))
            else:
                if not new_fill_value:
                    msg = "Fill value unchanged for '%s'" % basin
                else:
                    msg = "Updated fill value for '%s' from %s to %s" % (
                        basin, orig_fill, new_fill_value)
                self.stdout.write("%s\n" % msg)
