# Separate file for constants used in the controlnext app,
# so they are easily editable.
# Keep this separate from Django's settings file,
# because this code might need to be reused in a FEWS general adapter.
import datetime

jdbc_source_slug = 'controlnext'

rain_filter_id = 'neerslag_combo'    # Neerslag gecombimeerd
rain_location_id = 'OPP1'            # Oranjebinnenpolder Oost
rain_parameter_ids = {
    'min': 'P.min',   # Minimum
    'mean': 'P.gem',  # Gemiddeld
    'max': 'P.max'    # Maximum
}

fill_filter_id = 'waterstand_basins' # Waterstanden
fill_location_id = '467446797569'    # Van der Lans-west, niveau1
fill_parameter_id = 'WNS2820'        # Waterdiepte (cm)

frequency = datetime.timedelta(minutes=15)

min_berging_pct = 20
max_berging_pct = 100
max_berging_m3 = 20000 # in m^3
area_receiving_rain_m2 = 20000 # in m^2

def round_date(date):
    minutes = date.minute - (date.minute % 15)
    return date.replace(minute=minutes, second=0, microsecond=0)
