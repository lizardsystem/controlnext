def load_ipython_extension(ipython):
    import sys
    sys.path[0:0] = [
        '/home/jsmits/Development/repos/delfland',
        '/home/jsmits/.buildout/eggs/djangorecipe-1.3-py2.7.egg',
        '/home/jsmits/.buildout/eggs/Django-1.4.3-py2.7.egg',
        '/home/jsmits/.buildout/eggs/zc.recipe.egg-1.2.2-py2.7.egg',
        '/home/jsmits/.buildout/eggs/zc.buildout-1.4.4-py2.7.egg',
        '/usr/lib/python2.7/dist-packages',
        '/home/jsmits/.buildout/eggs/simplejson-2.4.0-py2.7-linux-x86_64.egg',
        '/home/jsmits/.buildout/eggs/Werkzeug-0.8.3-py2.7.egg',
        '/home/jsmits/.buildout/eggs/python_memcached-1.48-py2.7.egg',
        '/home/jsmits/.buildout/eggs/lizard_ui-4.16-py2.7.egg',
        '/home/jsmits/.buildout/eggs/lizard_map-4.16-py2.7.egg',
        '/home/jsmits/Development/repos/delfland/src/controlnext',
        '/home/jsmits/.buildout/eggs/gunicorn-0.13.4-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_nose-1.1-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_extensions-1.0.1-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_celery-3.0.11-py2.7.egg',
        '/home/jsmits/.buildout/eggs/South-0.7.6-py2.7.egg',
        '/home/jsmits/.buildout/eggs/raven-2.0.3-py2.7.egg',
        '/home/jsmits/.buildout/eggs/lizard_security-0.5-py2.7.egg',
        '/home/jsmits/.buildout/eggs/docutils-0.8-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_compressor-1.2-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_staticfiles-1.2.1-py2.7.egg',
        '/home/jsmits/.buildout/eggs/BeautifulSoup-3.2.1-py2.7.egg',
        '/home/jsmits/.buildout/eggs/pkginfo-0.8-py2.7.egg',
        '/home/jsmits/.buildout/eggs/mock-0.8.0-py2.7.egg',
        '/home/jsmits/.buildout/eggs/lizard_help-0.4-py2.7.egg',
        '/home/jsmits/.buildout/eggs/iso8601-0.1.4-py2.7.egg',
        '/home/jsmits/.buildout/eggs/djangorestframework-2.1.12-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_piston-0.2.2-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_jsonfield-0.8.11-py2.7.egg',
        '/home/jsmits/.buildout/eggs/Pillow-1.7.7-py2.7-linux-x86_64.egg',
        '/home/jsmits/.buildout/eggs/factory_boy-1.2.0-py2.7.egg',
        '/home/jsmits/.buildout/eggs/pandas-0.10.1-py2.7-linux-x86_64.egg',
        '/home/jsmits/.buildout/eggs/lizard_fewsjdbc-2.14-py2.7.egg',
        '/home/jsmits/.buildout/eggs/celery-3.0.11-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_tls-0.0.2-py2.7.egg',
        '/home/jsmits/.buildout/eggs/django_appconf-0.5-py2.7.egg',
        '/home/jsmits/.buildout/eggs/lizard_task-0.15-py2.7.egg',
        '/home/jsmits/.buildout/eggs/kombu-2.4.7-py2.7.egg',
        '/home/jsmits/.buildout/eggs/billiard-2.7.3.18-py2.7-linux-x86_64.egg',
        '/home/jsmits/.buildout/eggs/amqplib-1.0.2-py2.7.egg',
        '/home/jsmits/.buildout/eggs/anyjson-0.3.3-py2.7.egg',
        '/home/jsmits/Development/repos/delfland',
    ]

    from django.core.management.color import no_style
    from django_extensions.management.shells import import_objects
    imported_objects = import_objects(options={'dont_load': []},
        style=no_style())
    print imported_objects
    ipython.push(imported_objects)
