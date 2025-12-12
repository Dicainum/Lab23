from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "news/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        qs = Article.objects.filter(is_published=True)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q))
        return qs

class ArticleDetailView(DetailView):
    model = Article
    template_name = "news/article_detail.html"
    context_object_name = "article"