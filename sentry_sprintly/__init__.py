"""
sentry_sprintly
~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-sprintly').version
except Exception as e:
    VERSION = 'unknown'
