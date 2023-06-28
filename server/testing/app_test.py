import json
import pytest

from app import app, db, Bakery, BakedGood


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Create the database and tables
    with app.app_context():
        db.create_all()

    yield client

    # Drop the tables and remove the database
    with app.app_context():
        db.drop_all()


class TestApp:
    '''Flask application in flask_app.py'''

    def test_bakeries_route(self, client):
        '''has a resource available at "/bakeries".'''
        response = client.get('/bakeries')
        assert response.status_code == 200

    def test_bakeries_route_returns_json(self, client):
        '''provides a response content type of application/json at "/bakeries"'''
        response = client.get('/bakeries')
        assert response.content_type == 'application/json'

    def test_bakeries_route_returns_list_of_bakery_objects(self, client):
        '''returns JSON representing models.Bakery objects.'''
        with app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()

            response = client.get('/bakeries')
            data = json.loads(response.data.decode())
            assert type(data) == list
            for record in data:
                assert type(record) == dict
                assert record['id']
                assert record['name']
                assert record['created_at']

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route(self, client):
        '''has a resource available at "/bakeries/<int:id>".'''
        with app.app_context():
            b = Bakery(name="Bakery 1")
            db.session.add(b)
            db.session.commit()

            response = client.get('/bakeries/1')
            assert response.status_code == 200

            db.session.delete(b)
            db.session.commit()


    def test_bakery_by_id_route_returns_json(self, client):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        response = client.get('/bakeries/1')
        assert response.content_type == 'application/json'

    def test_bakery_by_id_route_returns_one_bakery_object(self, client):
        '''returns JSON representing one models.Bakery object.'''
        with app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()

            response = client.get('/bakeries/1')
            data = json.loads(response.data.decode())
            assert type(data) == dict
            assert data['id']
            assert data['name']
            assert data['created_at']

            db.session.delete(b)
            db.session.commit()

    def test_baked_goods_by_price_route(self, client):
        '''has a resource available at "/baked_goods/by_price".'''
        response = client.get('/baked_goods/by_price')
        assert response.status_code == 200

    def test_baked_goods_by_price_route_returns_json(self, client):
        '''provides a response content type of application/json at "/baked_goods/by_price"'''
        response = client.get('/baked_goods/by_price')
        assert response.content_type == 'application/json'

    def test_baked_goods_by_price_returns_list_of_baked_goods(self, client):
        '''returns JSON representing one models.Bakery object.'''
        with app.app_context():
            b = BakedGood(name="Madeleine", price=10)
            db.session.add(b)
            db.session.commit()

            response = client.get('/baked_goods/by_price')
            data = json.loads(response.data.decode())
            assert type(data) == list
            for record in data:
                assert record['id']
                assert record['name']
                assert record['price']
                assert record['created_at']

            db.session.delete(b)
            db.session.commit()

    def test_most_expensive_baked_good_route(self, client):
        '''has a resource available at "/baked_goods/most_expensive".'''
        with app.app_context():
            b1 = BakedGood(name="Madeleine", price=10)
            b2 = BakedGood(name="Croissant", price=15)
            db.session.add_all([b1, b2])
            db.session.commit()

            response = client.get('/baked_goods/most_expensive')
            assert response.status_code == 200

            db.session.delete_all([b1, b2])
            db.session.commit()
    
    def test_most_expensive_baked_good_route_returns_json(self, client):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        response = client.get('/baked_goods/most_expensive')
        assert response.content_type == 'application/json'

    def test_most_expensive_baked_good_route_returns_one_baked_good_object(self, client):
        '''returns JSON representing one models.BakedGood object.'''
        with app.app_context():
            b = BakedGood(name="Madeleine", price=10)
            db.session.add(b)
            db.session.commit()

            response = client.get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            assert type(data) == dict
            assert data['id']
            assert data['name']
            assert data['price']
            assert data['created_at']

            db.session.delete(b)
            db.session.commit()

    def test_most_expensive_baked_good_route_returns_most_expensive_baked_good_object(self, client):
        '''returns JSON representing one models.BakedGood object.'''
        with app.app_context():
            b = BakedGood(name="Madeleine", price=10)
            db.session.add(b)
            db.session.commit()

            response = client.get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            prices = [baked_good.price for baked_good in BakedGood.query.all()]
            highest_price = max(prices)

            assert data['price'] == highest_price

            db.session.delete(b)
            db.session.commit()


if __name__ == '__main__':
    pytest.main()
