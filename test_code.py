import run
import pytest
app = run.create_app()


def test_for_get():
    with app.test_client() as c:
        r = c.get('http://localhost:5000/api/properties')
        assert r.status_code == 200


def test_for_post():
    with app.test_client() as c:
        r = c.post('http://localhost:5000/api/properties')
        assert r.status_code == 200


def test_for_not_found_url():
    with app.test_client() as c:
        r = c.get('http://localhost:5000/api/')
        assert r.status_code == 404


def test_for_get_bad_url():
    with app.test_client() as c:
        r = c.get('http://localhost:5000/api/properties?page=adfgfhjg')
        assert r.status_code == 400


def test_for_page0():
    with app.test_client() as c:
        r = c.get('http://localhost:5000/api/properties?page=0')
        data = r.get_json()
        total = int(len(data))
        assert total == 48


def test_for_feed_page0():
    with app.test_client() as c:
        r = c.get('http://localhost:5000/api/properties?feed_ratio=[{"feed":11,"ratio":16},{"feed":12,"ratio":16},'
                  '{"feed":16,"ratio":16}]&page=0')
        data = r.get_json()
        total = int(len(data))
        assert total == 48
