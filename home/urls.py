from django.urls import path
from . import views
from django.views.generic import RedirectView  


urlpatterns = [
    path('', views.home, name="home"),
    path('workspaces/', views.workspaces, name="workspaces"),
    path('feature/', views.feature, name="feature"),
    path('tasks/', views.tasks, name="tasks"),
    path('feature.html', RedirectView.as_view(pattern_name='feature')),
     # About Us
    path('about-us/', views.about_us, name='about_us'),
    path('about_us.html', RedirectView.as_view(pattern_name='about_us')),

    # Blog
    path('blog/', views.blog, name='blog'),
    path('blog.html', RedirectView.as_view(pattern_name='blog')),

    # Contact
    path('contact/', views.contact, name='contact'),
    path('contact.html', RedirectView.as_view(pattern_name='contact')),

    # Documentation
    path('documentation/', views.documentation, name='documentation'),
    path('documentation.html', RedirectView.as_view(pattern_name='documentation')),

    # Help & Support
    path('help-support/', views.help_support, name='help_support'),
    path('help_support.html', RedirectView.as_view(pattern_name='help_support')),

    # Integrations
    path('integrations/', views.integrations, name='integrations'),
    path('integrations.html', RedirectView.as_view(pattern_name='integrations')),

    # Pricing
    path('pricing/', views.pricing, name='pricing'),
    path('pricing.html', RedirectView.as_view(pattern_name='pricing')),

    # Tutorial
    path('tutorial/', views.tutorial, name='tutorial'),
    path('tutorial.html', RedirectView.as_view(pattern_name='tutorial')),
]
