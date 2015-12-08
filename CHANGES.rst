Changelog of controlnext
===================================================


0.23 (unreleased)
-----------------

- Nothing changed yet.


0.22 (2015-12-08)
-----------------

- Added configurability for userprofiles. Now userprofiles can be preset with
 a temp_username, without users having to log in before setting their
 UserProfile.


0.21 (2015-12-08)
-----------------

- Bugfix changed 404 error into 403 error.


0.20 (2015-12-08)
-----------------
- Added SSO.
- Changed UserProfile model relation to grower to many to many.
- Updated model and views to allow for a many to one relation between grower and
  basin.
- Added logout buttons.
- Added login selector.
- Only link to url_slug when authorized.
- Added 403 when unauthorized instead of redirect to referer.


0.19 (2015-11-04)
-----------------

- Bugfixes for longer no-rain prediction graph.
- Limits the labels for the precipitation graph.


0.18 (2015-10-31)
-----------------

- Nothing changed yet.


0.17 (2015-10-31)
-----------------

- Longer graphs.


0.16 (2015-09-02)
-----------------

- Regression bugfix that stopped the calculate ('bereken') button from working.


0.15 (2015-08-25)
-----------------

- Total code cleanup. Controlnext site is now more up to date. Altered about
  10.000 lines of code.
- Added login with slug functionality


0.14 (2015-06-11)
-----------------

- Cm calculation changed to percentage.


0.13 (2013-12-12)
-----------------

- Nothing changed yet.


0.12 (2013-12-10)
-----------------

- Nothing changed yet.


0.11 (2013-12-10)
-----------------

- Add chartjs skin.
- Coonect the skin to the real data.


0.10 (2013-08-07)
-----------------

- Add reverse osmosis field to dashboard.


0.9 (2013-02-14)
----------------

- Add service class for consuming Wageneningen University's waterdemand
  JSON webservice.


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

