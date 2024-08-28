import pytest
import requests
from main import check_age, check_auth, get_cost

@pytest.mark.parametrize('age, expected', [
    (10, 'Доступ запрещён'),
    (18, 'Доступ разрешён'),
    (20, 'Доступ разрешён'),
])
def test_check_age(age, expected):
    assert check_age(age) == expected

@pytest.mark.parametrize('login, password, expected', [
    ('user', 'password', 'Доступ ограничен'),
    ('admin', '123', 'Доступ ограничен'),
    ('admin', 'password', 'Добро пожаловать'),
    ('', '', 'Доступ ограничен'),
])
def test_check_auth(login, password, expected):
    assert check_auth(login, password) == expected

@pytest.mark.parametrize('weight, expected', [
    (9, 'Стоимость доставки: 200 руб.'),
    (10, 'Стоимость доставки: 200 руб.'),
    (11, 'Стоимость доставки: 500 руб.'),
    (12, 'Стоимость доставки: 500 руб.'),
])
def test_get_cost(weight, expected):
    assert get_cost(weight) == expected


class TestYandexDisk:
    def setup_method(self):

        self.valid_headers = {
            'Authorization': 'OAuth y0_AgAAAAB4U_jYAADLWwAAAAEPL9NWAABByVRHr7ZGFJldiMqfVEOVROeYrw'
        }
        self.invalid_headers = {
            'Authorization': 'OAuth invalid_token'
        }

    @pytest.mark.parametrize(
        'key,value,status_code',
        (
            ['pat', 'Image', 400],
            ['path', 'Image', 201],
            ['path', 'Image', 409],
        )
    )
    def test_create_folder(self, key, value, status_code):
        params = {key: value}
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                headers=self.valid_headers,
                                params=params)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        'path,status_code',
        [
            ('Invalid/Path/With?Invalid*Chars', 400),
            ('/valid_path', 401),
        ]
    )
    def test_invalid_path_or_token(self, path, status_code):
        headers = self.invalid_headers if status_code == 401 else self.valid_headers
        params = {'path': path}
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                headers=headers,
                                params=params)
        assert response.status_code == status_code