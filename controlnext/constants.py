# Separate file for constants used in the controlnext app,
# so they are easily editable.
# Keep this separate from Django's settings file,
# because this code might need to be reused in a FEWS general adapter.

# legacy code used for single grower demo
# TODO: remove this module completely

rain_filter_id = 'neerslag_combo'     # Neerslag gecombimeerd
rain_location_id = 'OPP1'             # Oranjebinnenpolder Oost

fill_filter_id = 'waterstand_basins'  # Waterstanden
fill_location_id = '467446797569'     # Van der Lans-west, niveau1
fill_parameter_id = 'WNS2820'         # Waterdiepte (cm)

min_berging_pct = 20
max_berging_pct = 100
max_berging_m3 = 15527  # in m^3
opp_invloed_regen_m2 = 94000  # in m^2
max_uitstroom_per_tijdstap_m3 = 4.5  # in m^3
bovenkant_bak_cm = 265  # in cm
hoogte_niveaumeter_cm = 265  # in cm
