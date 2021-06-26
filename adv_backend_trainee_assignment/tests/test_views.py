import json

from django.test import TestCase


class TestViews(TestCase):
    def setUp(self):
        url = 'http://127.0.0.1:8000/api/v1/ads/'
        data = json.dumps({"title": "1",
                           "description": "1",
                           "urls_list": "https://hfd.com,http://abc.ru,https://gdfhdk.ru",
                           "price": 1000})
        self.client.post(url, data=data, content_type='application/json')

    # Тесты метода получения конкретного объявления:
    def test_get_exist_ad(self):
        id = 1
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/{id}/')
        self.assertEqual(resp.status_code, 200)
    
    def test_get_not_exist_ad(self):
        id = 999
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/{id}/')
        self.assertEqual(resp.status_code, 404)

    # Тесты метода получения списка объявлений:
    def test_get_ad_list(self):
        page = 1
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}')
        self.assertEqual(resp.status_code, 200)
    
    def test_get_ad_list_with_order_desc(self):
        page = 1
        order = 'desc'
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}&order={order}')
        self.assertEqual(resp.status_code, 200)
    
    def test_get_ad_list_with_sort_by_date(self):
        page = 1
        sort_by = 'date'
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}&sorted={sort_by}')
        self.assertEqual(resp.status_code, 200)
    
    def test_get_ad_list_with_sort_by_date_desc(self):
        page = 1
        order = 'desc'
        sort_by = 'date'
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}&sorted={sort_by}&order={order}')
        self.assertEqual(resp.status_code, 200)
    
    def test_get_ad_list_with_sort_by_another_db_field(self):
        page = 1
        sort_by = 'title'
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}&sorted={sort_by}')
        self.assertEqual(resp.status_code, 400)
    
    def test_get_ad_list_with_no_page(self):
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/')
        self.assertEqual(resp.status_code, 400)

    def test_get_ad_list_with_page_as_str(self):
        page = 'a'
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}')
        self.assertEqual(resp.status_code, 400)
    
    def test_get_ad_list_length(self):
        page = 1
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/ads/list/?page={page}').json()
        assert len(resp) <= 10

    # Тесты метода создания объявления:
    def test_add_ad_with_incorrect_types(self):
        url = 'http://127.0.0.1:8000/api/v1/ads/'
        title_is_int = 1
        data = json.dumps({"title": title_is_int,
                           "description": "1",
                           "urls_list": "https://hfd.com,http://abc.ru,https://gdfhdk.ru",
                           "price": 1000})
        resp = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_add_ad_with_incorrect_urls(self):
        url = 'http://127.0.0.1:8000/api/v1/ads/'
        incorrect_urls = 'https://hfd.comhttp://abc.ruhttps://gdfhdk.ru'
        data = json.dumps({"title": "1",
                           "description": "1",
                           "urls_list": incorrect_urls,
                           "price": 1000})
        resp = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
    
    def test_add_ad_with_more_than_3_urls(self):
        url = 'http://127.0.0.1:8000/api/v1/ads/'
        more_than_3_urls = 'https://hfd.com,http://abc.ru,https://gdfhdk.ru,http://def.com'
        data = json.dumps({"title": "1",
                           "description": "1",
                           "urls_list": more_than_3_urls,
                           "price": 1000})
        resp = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
    
    def test_add_correct_ad(self):
        url = 'http://127.0.0.1:8000/api/v1/ads/'
        data = json.dumps({"title": "1",
                           "description": "1",
                           "urls_list": "https://hfd.com,http://abc.ru,https://gdfhdk.ru",
                           "price": 1000})
        resp = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)