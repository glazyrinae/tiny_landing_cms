from django.test import TestCase, override_settings

from .models import Landing


@override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=["testserver"])
class SeoTests(TestCase):
    def test_robots_txt_contains_search_engine_rules(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response["Content-Type"])

        body = response.content.decode()
        self.assertIn("User-agent: *", body)
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Disallow: /send-feedback/", body)
        self.assertIn("Clean-param: utm_source", body)
        self.assertIn("utm_source&utm_medium", body)
        self.assertNotIn("&amp;", body)
        self.assertIn("Sitemap: https://example.com/sitemap.xml", body)
        self.assertNotRegex(body, r"[А-Яа-яЁё]")

    def test_sitemap_xml_contains_canonical_home_url(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/xml", response["Content-Type"])
        self.assertContains(response, "<loc>https://example.com/</loc>")

    def test_home_page_has_core_seo_tags(self):
        Landing.objects.create(
            title="Физрук",
            desc="Современный фитнес-клуб с персональными тренировками и абонементами.",
            footer="Фитнес-клуб Физрук",
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="ru">')
        self.assertContains(response, "<title>Фитнес-клуб Физрук</title>")
        self.assertContains(
            response,
            '<link rel="canonical" href="https://example.com/">',
        )
        self.assertContains(response, 'property="og:type" content="website"')
        self.assertContains(response, 'type="application/ld+json"')
