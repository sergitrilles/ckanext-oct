from collections import OrderedDict

import pylons

from jinja2 import Undefined

from ckan.lib.activity_streams import \
    activity_stream_string_functions as activity_streams

def most_recent_datasets(num=3):
    """Return a list of recent datasets."""

    # the current_package_list_with_resources action returns private resources
    # which need to be filtered

    datasets = []
    i = 0
    while len(datasets) < num:
        datasets += filter(lambda ds: not ds['private'],
                           tk.get_action('current_package_list_with_resources')({},
                                         {'limit': num, 'offset': i * num}))
        i += 1

    return datasets[:num]


def apps(featured_only=True):
    """Return apps for all datasets."""

    apps = tk.get_action('related_list')({}, {'type_filter': 'application',
                                              'featured': featured_only})

    return apps


def dataset_count():
    """Return a count of all datasets"""

    result = tk.get_action('package_search')({}, {'rows': 1})
    return result['count']


def groups():
    """Return a list of groups"""

    return tk.get_action('group_list')({}, {'all_fields': True})




# monkeypatch activity streams
activity_streams['changed group'] = (
    lambda c, a: tk._("{actor} updated the topic {group}")
)

activity_streams['deleted group'] = (
    lambda c, a: tk._("{actor} deleted the topic {group}")
)

activity_streams['new group'] = (
    lambda c, a: tk._("{actor} created the topic {group}")
)



#init
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class OctPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
	
	plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IRoutes)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'oct')
		
	def get_helpers(self):
        """Register odp_theme_* helper functions"""

        return {'oct_most_recent_datasets': most_recent_datasets,
                'oct_dataset_count': dataset_count,
                'oct_groups': groups,
                'oct_apps': apps}