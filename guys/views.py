from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import render, redirect
from guys.forms import FloodForm, NewsForm, CategoryForm, TopicForm, TopicMessagesForm
from guys.models import FloodMessages, News, Category, Topic

menu = [{'title': "Флудилка", 'url_name': 'flood'},
        {'title': "Новости", 'url_name': 'news'},
        {'title': "Темы для обсуждения", 'url_name': 'topic'},
        {'title': "Поддержка", 'url_name': 'support'},
        {'title': "О сайте", 'url_name': 'about'},
        ]


def index(request):
    data = {'title': "Главная страница сайта", 'menu': menu, }
    return render(request, 'guys/index.html', data)


def news(request):
    news_post = News.objects.all().order_by('-time_drop')
    return render(request, 'guys/news.html', {'title': "Новости",
                                              'menu': menu, 'news': news_post})


@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm()
    return render(request, 'guys/add_news.html', {'title': "Добавление новости",
                                                  'menu': menu, 'form': form})


@login_required
def flood(request):
    if request.method == 'POST':
        form = FloodForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('flood')
    else:
        form = FloodForm()
    messages = FloodMessages.objects.all().order_by('time_drop')[:50]
    return render(request, 'guys/flood.html', {'title': "Флудилка",
                                               'menu': menu, 'messages': messages, 'form': form})


def support(request):
    return render(request, 'guys/support.html', {'title': "Поддержка", 'menu': menu, })


def topic(request):
    categories = Category.objects.all()
    return render(request, 'guys/topic.html',
                  {'title': "Темы для обсуждения", 'menu': menu, 'categories': categories})


def topic_category(request, category_id):
    category = Category.objects.get(id=category_id)
    topics = Topic.objects.filter(category=category)
    return render(request, 'guys/topic_category.html',  {'title': "Категории тем",
        'category': category,'topics': topics,'menu': menu,})


def add_topic(request, category_id):
    category =  Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topics = form.save(commit=False)
            topics.category = category
            topics.author = request.user
            topics.save()
            return redirect('topic_category', category_id=category.id)
    else:
        form = TopicForm()
    return render(request, 'guys/add_topic.html',
                      {'title': "Добавление темы", 'menu': menu, 'form': form, 'category': category,})


def topic_discussion(request, topic_id):
    topic_dis = Topic.objects.get(id=topic_id)
    if request.method == 'POST':
        form = TopicMessagesForm(request.POST)
        if form.is_valid():
            dis = form.save(commit=False)
            dis.topic = topic_dis
            dis.author = request.user
            dis.save()
            return redirect('topic_discussion', topic_id)
    else:
        form = TopicMessagesForm()
    return render(request, 'guys/topic_discussion.html', {'topic_dis': topic_dis,'form': form })


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topic')
    else:
        form = CategoryForm()
    return render(request, 'guys/add_category.html',
                  {'title': "Добавление раздела", 'menu': menu, 'form': form})


def about(request):
    return render(request, 'guys/about.html', {'title': "О сайте", 'menu': menu, })
