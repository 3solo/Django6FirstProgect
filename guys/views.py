from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from guys.forms import FloodForm, NewsForm, CategoryForm, TopicForm, TopicMessagesForm
from guys.models import FloodMessages, News, Category, Topic

menu = [{'title': "Общий чат", 'url_name': 'flood'},
        {'title': "Новости", 'url_name': 'news'},
        {'title': "Темы для обсуждения", 'url_name': 'topic'},
        {'title': "Поддержка", 'url_name': 'support'},
        {'title': "О сайте", 'url_name': 'about'},
        ]


class IndexView(TemplateView):
    template_name = 'guys/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Главная страница сайта'
        context['menu'] = menu
        return context


class NewsView(ListView):
    model = News
    template_name = 'guys/news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.all().order_by('-time_drop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Новости'
        context['menu'] = menu
        return context


class AddNewsView(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'guys/add_news.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Добавление новости'
        context['menu'] = menu
        return context


class FloodView(LoginRequiredMixin, ListView):
    model = FloodMessages
    template_name = 'guys/flood.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return FloodMessages.objects.all().order_by('time_drop')[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Общий чат'
        context['menu'] = menu
        context['form'] = FloodForm()
        return context

    def post(self,request):
        form = FloodForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('flood')

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class SupportView(TemplateView):
    template_name = 'guys/support.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Поддержка'
        context['menu'] = menu
        return context


class TopicView(ListView):
    model = Category
    template_name = 'guys/topic.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Темы для обсуждения'
        context['menu'] = menu
        return context


class TopicCategoryView(DetailView):
    model = Category
    template_name = 'guys/topic_category.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории тем'
        context['menu'] = menu
        context['topics'] = Topic.objects.filter(category=self.object)
        return context


class AddTopicView(LoginRequiredMixin, CreateView):
    form_class = TopicForm
    template_name = 'guys/add_topic.html'
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, id=kwargs['category_id'])
        return super().dispatch(request, **kwargs)

    def form_valid(self, form):
        topics = form.save(commit=False)
        topics.category = self.category
        topics.author = self.request.user
        topics.save()
        return redirect('topic_category', category_id=self.category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление темы"
        context['menu'] = menu
        context['category'] = self.category
        return context


class TopicDiscussion(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = 'guys/topic_discussion.html'
    context_object_name = 'topic_dis'
    pk_url_kwarg = 'topic_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TopicMessagesForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TopicMessagesForm(request.POST)
        if form.is_valid():
            dis = form.save(commit=False)
            dis.topic = self.object
            dis.author = request.user
            dis.save()
            return redirect('topic_discussion', self.object.id)

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class AddCategoryView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'guys/add_category.html'
    success_url = reverse_lazy('topic')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление раздела"
        context['menu'] = menu
        return context


class AboutView(TemplateView):
    template_name = 'guys/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'О сайте'
        context['menu'] = menu
        return context
