from django.urls import path
from guys import views

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'home'),
    path('news/', views.NewsView.as_view(), name = 'news'),
    path('flood/', views.FloodView.as_view(), name= 'flood'),
    path('support/', views.SupportView.as_view(), name= 'support'),
    path('topic/', views.TopicView.as_view(), name = 'topic'),
    path('about/',views.AboutView.as_view(), name = 'about'),
    path('add-category/', views.AddCategoryView.as_view(), name ='add_category'),
    path('add-news/',views.AddNewsView.as_view(), name = 'add_news'),
    path('topic/<int:category_id>',views.TopicCategoryView.as_view(), name = 'topic_category'),
    path('topic/<int:category_id>/add',views.AddTopicView.as_view(), name = 'add_topic'),
    path('topic/<int:topic_id>/discussion',views.TopicDiscussion.as_view(), name = 'topic_discussion'),
]