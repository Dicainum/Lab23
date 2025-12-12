from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from news.models import Article


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.article = Article.objects.create(
            title="Test Article",
            content="Some content",
            author=self.user,
            is_published=True,
        )

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_article_fields(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.content, "Some content")
        self.assertEqual(self.article.author.username, "testuser")
        self.assertTrue(self.article.is_published)
        self.assertIsNotNone(self.article.created_at)
        self.assertIsNotNone(self.article.updated_at)


class ArticleListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass")

        Article.objects.create(
            title="News One",
            content="Content 1",
            author=self.user,
            is_published=True,
        )
        Article.objects.create(
            title="Another News",
            content="Content 2",
            author=self.user,
            is_published=True,
        )
        Article.objects.create(
            title="Hidden",
            content="Secret",
            author=self.user,
            is_published=False,
        )

    def test_home_page_status_code(self):
        response = self.client.get(reverse('news:list'))
        self.assertEqual(response.status_code, 200)

    def test_only_published_articles_displayed(self):
        response = self.client.get(reverse('news:list'))
        articles = response.context['articles']
        self.assertEqual(len(articles), 2)
        titles = [article.title for article in articles]
        self.assertNotIn("Hidden", titles)

    def test_search_filter(self):
        response = self.client.get(reverse('news:list') + "?q=one")
        articles = response.context['articles']
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "News One")


class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="pass")
        self.article = Article.objects.create(
            title="Detail Test",
            content="Full content",
            author=self.user,
            is_published=True,
        )

    def test_detail_page_status_code(self):
        response = self.client.get(reverse("news:detail", args=[self.article.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_content(self):
        response = self.client.get(reverse("news:detail", args=[self.article.id]))
        self.assertContains(response, "Detail Test")
        self.assertContains(response, "Full content")
        self.assertContains(response, "author")


class AdminAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

    def test_admin_login(self):
        login = self.client.login(username="admin", password="adminpass")
        self.assertTrue(login)

    def test_admin_page_access(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
