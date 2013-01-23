Changelog of controlnext
===================================================


0.4 (unreleased)
----------------

- Nothing changed yet.


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

