""":mod:`buzzword_bingo_client.core.api` --- API to interface with the REST API

.. todo::

    Add more logging to the API module.

.. todo::

    Definitely look at `Slumber <http://slumber.in/>`_ for creating APIs instead
    of the horrible mess I have right now.

"""

from __future__ import print_function
import slumber

YAML_MIME = 'application/yaml'
HTTP_SCHEME = 'http://'

import logging
logger = logging.getLogger(__name__)
"""Module-level logger."""

class API(object):
    """Interface to buzzword bingo server. Internally uses `slumber`_ to create
    a :class:`slumber.API` object and provides thin wrappers around that.

    .. _slumber: http://slumber.in/
    """
    def __init__(self, base_url):
        """Create an API object.
        
        :param base_url: REST API base URL
        :type base_url: :class:`str`
        """
        logger.debug('Instance created with base URL `{0}\''.format(base_url))
        self.slumber_api = slumber.API(base_url)

    def all_boards(self):
        """Return all boards."""
        return self.slumber_api.boards.get()

    def load_url(self, url):
        """Load an object from an arbitrary URL.

        :param url: URL to load
        :type url: :class:`str`
        :return: the object at the URL
        :rtype: :class:`object`
        """
        # made up the `arbitrary' resource just to have a
        # resource on which to use the `url_override'
        # keyword
        self.slumber_api.arbitrary(url_override=url)

    def load_dictionary(self, item):
        """Recursively replace hypermedia in a dictionary with an object by
        fetching the actual object.
        
        :param item: the dictionary item containing hypermedia
        :type item: :class:`dict`
        :returns: the loaded dictionary item
        """
        for key, val in item.iteritems():
            # skip keys name `url': these contain the url of the object
            if key == 'url':
                continue
            if (type(val) is list and len(val) >
                0 and val[0].startswith(HTTP_SCHEME)):
                new_list = []
                for url in val:
                    new_list.append(self.load_dictionary(self.load_url(url)))
                item[key] = new_list
            elif type(val) is str and val.startswith(HTTP_SCHEME):
                item[key] = self.load_dictionary(self.load_url(val))
        return item
