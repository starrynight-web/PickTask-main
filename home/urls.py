from django.urls import path
from . import views
from django.views.generic import RedirectView  


urlpatterns = [
    path('', views.home, name="home"),
    #path('workspaces/', views.workspaces, name="workspaces"),
    path('feature/', views.feature, name="feature"),
    #path('tasks/', views.tasks, name="tasks"),
    path('feature.html', RedirectView.as_view(pattern_name='feature')),
    
    path('about_us/', views.about_us, name='about_us'),
    path('about_us.html', RedirectView.as_view(pattern_name='about_us')),

    path('blog/', views.blog, name='blog'),
    path('blog.html', RedirectView.as_view(pattern_name='blog')),

 
    path('contact/', views.contact, name='contact'),
    path('contact.html', RedirectView.as_view(pattern_name='contact')),

 
    path('documentation/', views.documentation, name='documentation'),
    path('documentation.html', RedirectView.as_view(pattern_name='documentation')),

  
    path('help_support/', views.help_support, name='help_support'),
    path('help_support.html', RedirectView.as_view(pattern_name='help_support')),

   
    path('integrations/', views.integrations, name='integrations'),
    path('integrations.html', RedirectView.as_view(pattern_name='integrations')),


    path('pricing/', views.pricing, name='pricing'),
    path('pricing.html', RedirectView.as_view(pattern_name='pricing')),

   
    path('tutorial/', views.tutorial, name='tutorial'),
    path('tutorial.html', RedirectView.as_view(pattern_name='tutorial')),
]
