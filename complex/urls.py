from django.urls import path

from complex import views


urlpatterns = [
    path('', views.home, name='home'),
    path('complexes-list/', views.complexes_list, name='complexes-list'),
    path('category/<slug:category_slug>/', views.complexes_list, name='complexes_by_category'),
    path('category/<slug:category_slug>/<slug:complex_slug>/', views.complexes_detail, name='complex_detail'),
    path('category/<slug:category_slug>/<slug:complex_slug>/sessions', views.session_list, name='session-list'),
    path('create-complex/', views.create_complex, name='create-complex'),
    path('edit-complex/<slug:complex_slug>/',views.edit_complex,name='edit-complex'),
    path('category/<slug:category_slug>/<slug:complex_slug>/create-session/', views.create_sessions,
         name='create-session'),
    path('category/<slug:category_slug>/<slug:complex_slug>/<int:session_id>/edit-session/',
         views.edit_session, name='edit_session'),
    path('search/', views.search, name='search'),
]


