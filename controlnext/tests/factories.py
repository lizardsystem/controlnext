import factory

from ..models import GrowerInfo


class GrowerInfoFactory(factory.Factory):

    FACTORY_FOR = GrowerInfo

    name = 'Lans'
    crop = 'tomato'
    crop_surface = 94000

    fill_filter_id = 'waterstand_basins'
    fill_parameter_id = 'WNS2820'
    fill_location_id = '467446797569'

    rain_filter_id = 'neerslag_combo'
    rain_location_id = 'OPP1'


