import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import pylons

##def most_recent_datasets(num=3):
##    """Return a list of recent datasets."""
##
##    # the current_package_list_with_resources action returns private resources
##    # which need to be filtered
##
##    datasets = []
##    i = 0
##    while len(datasets) < num:
##        datasets += filter(lambda ds: not ds['private'],
##                           toolkit.get_action('current_package_list_with_resources')({},
##                                         {'limit': num, 'offset': i * num}))
##        i += 1
##
##    return datasets[:num]

def most_recent_datasets(limit=3):
    datasets = toolkit.get_action('package_search')(
        data_dict={'sort': 'metadata_modified desc', 'rows':limit})
    return datasets.get('results')

def apps(featured_only=True):
    """Return apps for all datasets."""

    apps = toolkit.get_action('related_list')({}, {'type_filter': 'application',
                                              'featured': featured_only})

    return apps


def dataset_count():
    """Return a count of all datasets"""

    result = toolkit.get_action('package_search')({}, {'rows': 1})
    return result['count']


def groups():
    """Return a list of groups"""

    return toolkit.get_action('group_list')({}, {'all_fields': True})


class OctPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)


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
