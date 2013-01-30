Changelog of controlnext
===================================================


0.9 (unreleased)
----------------

- Nothing changed yet.


0.8 (2013-01-30)
----------------

- Add grower's own meter fields to Basin and make a FEWS method for querying the related data.
- Add comparison plot for basins with their own water level meters.


0.7 (2013-01-29)
----------------

- Move basin specific data from GrowerInfo to Basin model.


0.6 (2013-01-28)
----------------

- Add intro and travis status image.
- Add image field to GrowerInfo model. 


0.5 (2013-01-28)
----------------

- Change test infrastructure to be able to test offline and prepare for 
  better tests (without fews connection).
- Make current test(s) work with the mocked test data.
- Add .travis.yml.
- Add WURService class to consume Wageningen University webservice.


0.4 (2013-01-23)
----------------

- Add controlnext_demo app to MANIFEST.in in order to get its templates dir
  packages as well.
- Update missing setup.py fields.
- Add simple test factory for GrowerInfo.


0.3 (2013-01-23)
----------------

- Added support for djangorestframeworks 2.x branch.
- Add on_main_map field to Basin model.
- Fixed DATABASE and INSTALLED_APPS testsettings.
- Prepared jQuery UI paths, which have slightly changed in the new lizard-ui.
- Ensured URLs of dependencies (/map, /ui) aren't included twice when running
  as part of a site.
- Add link to grower dashboard in popup, after clicking a basin.
- Set initial desired fill slide value to the current fill value.

0.2 (2012-12-18)
----------------

- Use pad method for pandas fillna call, because fillna(None) is not allowed
anymore since pandas 0.10.0.


0.1 (2012-12-18)
----------------

- Initial project structure created with nensskel 1.26.dev0.
- Add functionality for multiple basins / growers.
- Show default map with basin fill icons and info on hover.

