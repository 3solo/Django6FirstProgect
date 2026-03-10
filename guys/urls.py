from django.urls import path
from guys import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('news/', views.news, name = 'news'),
    path('flood/', views.flood, name= 'flood'),
    path('support/', views.support, name= 'support'),
    path('topic/', views.topic, name = 'topic'),
    path('about/',views.about, name = 'about'),
    path('add-category/', views.add_category, name ='add_category'),
    path('add-news/',views.add_news, name = 'add_news'),
    path('topic/<int:category_id>',views.topic_category, name = 'topic_category'),
    path('topic/<int:category_id>/add',views.add_topic, name = 'add_topic'),
    path('topic/<int:topic_id>/discussion',views.topic_discussion, name = 'topic_discussion'),
]