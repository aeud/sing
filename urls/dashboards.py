from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'apps.dashboards.views.index', name='dashboards_index'),
    url(r'^new$', 'apps.dashboards.views.new', name='dashboards_new'),
    url(r'^create$', 'apps.dashboards.views.create', name='dashboards_create'),
    url(r'^my-dashboards$', 'apps.dashboards.views.my', name='dashboards_my'),
    url(r'^(?P<dashboard_id>\d+)/$', 'apps.dashboards.views.show', name='dashboards_show'),
    url(r'^(?P<dashboard_slug>[a-z0-9\-]+)/$', 'apps.dashboards.views.play', name='dashboards_play'),
    url(r'^(?P<dashboard_id>[a-z0-9\-]+)/play/(?P<token>[\w\-]+)$', 'apps.dashboards.views.play_anonymous', name='dashboards_play_anonymous'),
    url(r'^(?P<dashboard_id>\d+)/edit$', 'apps.dashboards.views.edit', name='dashboards_edit'),
#    url(r'^(?P<dashboard_id>\d+)/schedule$', 'apps.dashboards.views.schedule', name='dashboards_schedule'),
#    url(r'^(?P<dashboard_id>\d+)/schedule-post$', 'apps.dashboards.views.schedule_post', name='dashboards_schedule_post'),
    url(r'^(?P<dashboard_id>\d+)/update$', 'apps.dashboards.views.update', name='dashboards_update'),
    url(r'^(?P<dashboard_id>\d+)/star$', 'apps.dashboards.views.star', name='dashboards_star'),
    url(r'^(?P<dashboard_id>\d+)/unstar$', 'apps.dashboards.views.unstar', name='dashboards_unstar'),
    url(r'^(?P<dashboard_id>\d+)/positions$', 'apps.dashboards.views.positions', name='dashboards_positions'),
    url(r'^(?P<dashboard_id>\d+)/remove$', 'apps.dashboards.views.remove', name='dashboards_remove'),
    url(r'^(?P<dashboard_id>\d+)/hard-remove$', 'apps.dashboards.views.hard_remove', name='dashboards_hard_remove'),
    url(r'^(?P<dashboard_id>\d+)/visualizations/new$', 'apps.dashboards.views.visualization_new', name='dashboards_visualizations_new'),
    url(r'^(?P<dashboard_id>\d+)/visualizations/create$', 'apps.dashboards.views.visualization_create', name='dashboards_visualizations_create'),
    url(r'^(?P<dashboard_id>\d+)/visualizations/(?P<dashboard_entity_id>\d+)/edit$', 'apps.dashboards.views.visualization_edit', name='dashboards_visualizations_edit'),
    url(r'^(?P<dashboard_id>\d+)/visualizations/(?P<dashboard_entity_id>\d+)/update$', 'apps.dashboards.views.visualization_update', name='dashboards_visualizations_update'),
    url(r'^(?P<dashboard_id>\d+)/visualizations/(?P<dashboard_entity_id>\d+)/remove$', 'apps.dashboards.views.visualization_remove', name='dashboards_visualizations_remove'),
    url(r'^(?P<dashboard_id>\d+)/sort$', 'apps.dashboards.views.sort', name='dashboards_sort'),
    url(r'^(?P<dashboard_id>\d+)/export$', 'apps.dashboards.views.d_export', name='dashboards_export'),
    url(r'^(?P<dashboard_id>\d+)/share$', 'apps.dashboards.views.share', name='dashboards_share'),
    url(r'^import$', 'apps.dashboards.views.d_import', name='dashboards_import'),
    url(r'^import/post$', 'apps.dashboards.views.d_import_post', name='dashboards_import_post'),
#    url(r'^(?P<visualization_id>\d+)/query$', 'apps.visualizations.views.query', name='visualizations_query'),
#    url(r'^(?P<visualization_id>\d+)/query/update$', 'apps.visualizations.views.query_update', name='visualizations_query_update'),
#    url(r'^(?P<visualization_id>\d+)/graph$', 'apps.visualizations.views.graph', name='visualizations_graph'),
#    url(r'^(?P<visualization_id>\d+)/graph/update$', 'apps.visualizations.views.graph_update', name='visualizations_graph_update'),
#    url(r'^(?P<visualization_id>\d+)/execute$', 'apps.visualizations.views.execute', name='visualizations_execute'),
#    url(r'^(?P<visualization_id>\d+)/remove$', 'apps.visualizations.views.remove', name='visualizations_remove'),
]