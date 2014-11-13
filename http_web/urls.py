from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'http_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^look/(\d+\.\d+\.\d+\.\d+)/(.*)/(\w+)','http_web.views.look'),
    url(r'^$','http_web.views.index' ),
    url(r'^test/','http_web.views.test' ),
    url(r'^index/','http_web.views.index' ),
    url(r'^search/','http_web.views.search' ),
    url(r'^feiyong/(\d+\.\d+\.\d+\.\d+)/','http_web.views.feiyong' ),
    url(r'^tj/(\d+\.\d+\.\d+\.\d+)/(.*)/','http_web.views.calc_sum'),
    url(r'^out/','http_web.views.out'),
    url(r'^bgindex/','http_web.bg.index'),
    url(r'^sqllook/','http_web.views.looksql'),
	
    
    url(r'^bg/','http_web.bg.index_add'),
    url(r'^bgdel/(.*)','http_web.bg.index_del'),
    url(r'^bgadd/','http_web.bg.add_data'),
    url(r'^bgdeldo/','http_web.bg.del_data'),
    url(r'^bmlook/(\d+)/(\d{4}-\d{2}-\d{2})/(\w+)','http_web.views.bmlook'),
)
