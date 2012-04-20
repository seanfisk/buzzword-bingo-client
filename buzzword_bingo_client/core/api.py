""":mod:`buzzword_bingo_client.core.api` --- API to interface with the REST API

.. todo::

    Add more logging to the API module.

"""

from __future__ import print_function
import requests

YAML_MIME = 'application/yaml'
HTTP_SCHEME = 'http://'

import logging
logger = logging.getLogger(__name__)
"""Module-level logger."""

import yaml
try:
    # try to use LibYAML (C-based) if we have it
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    # otherwise, fall back to pure Python
    from yaml import Loader, Dumper

class API(object):
    """Interface to buzzword bingo server."""
    def __init__(self, base_url):
        """Create an API object.
        
        :param base_url: REST API base URL
        :type base_url: :class:`str`
        """
        self._base_url = base_url
        logger.debug('Instance created with base URL `{0}\''.format(
            self._base_url))
        self.session = requests.session(headers={'Accept', YAML_MIME})

    def _absolute_url(self, relative_url):
        """Return the relative url prepended with the base url, giving the full
        url.
        
        :param relative_url: URL suffix
        :type relative_url: :class:`str`
        :returns: full URL
        :rtype: :class:`str`
        """
        return self._base_url + relative_url

    def all_boards(self):
        """Return all boards.
        """
        response = self.session.get(self._absolute_url('boards/'))
        seq = yaml.safe_load(response.text)
        for i, item in enumerate(seq):
            seq[i] = self._fill_item(item)
        return seq

    def _fill_item(self, item):
        """Recursively replace hypermedia in a dictionary with an object by
        fetching the actual object.
        
        :param item: the item containing hypermedia
        :type item: :class:`dict`
        """
        for key, val in item.iteritems():
            # skip keys name `url': these contain the url of the object
            if key == 'url':
                continue
            if (type(val) is list and len(val) >
                0 and val[0].startswith(HTTP_SCHEME)):
                new_list = []
                for url in val:
                    new_list.append(
                        self._fill_item(
                            yaml.safe_load(self.session.get(url).text)))
                item[key] = new_list
            elif type(val) is str and val.startswith(HTTP_SCHEME):
                item[key] = self._fill_item(
                    yaml.safe_load(self.session.get(val).text))
        return item
