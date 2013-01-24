import factory

try:
    # new style
    from lizard_fewsjdbc.tests.factories import JdbcSourceFactory
except ImportError:
    # old style
    from lizard_fewsjdbc.tests import JdbcSourceF as JdbcSourceFactory

from controlnext.models import GrowerInfo, Basin


class GrowerInfoFactory(factory.Factory):
    """Factory for generating GrowerInfo test instances."""
    FACTORY_FOR = GrowerInfo

    name = 'Lans'
    crop = 'tomato'
    crop_surface = 94000

    fill_filter_id = 'waterstand_basins'
    fill_parameter_id = 'WNS2820'
    fill_location_id = '467446797569'

    rain_filter_id = 'neerslag_combo'
    rain_location_id = 'OPP1'

    max_storage = 15527
    min_storage_pct = 20
    max_storage_pct = 100
    rain_flood_surface = 94000

    max_outflow_per_timeunit = 4.5
    basin_top = 265
    level_indicator_height = 265

    jdbc_source = factory.SubFactory(JdbcSourceFactory)


class BasinFactory(factory.Factory):
    """Factory for generating Basin test instances."""
    FACTORY_FOR = Basin

    owner = factory.SubFactory(GrowerInfoFactory)
    name = 'Basin 1'

    current_fill = 13350
