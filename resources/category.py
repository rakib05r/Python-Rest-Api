from flask_restful import Resource
from pymongo import MongoClient
from faker import Faker
from flask import request
import pymongo
import ast
import random


client = MongoClient('mongodb://localhost:27017/')
db = client['property-database_1']
collection = db['property-collection_1']


class Category(Resource):

    # Property Inserting Part

    def post(self):
        feed = [11, 12, 16]
        fake = Faker()
        for i in range(0, 300):
            value = {
                'id': i,
                'feed': random.choice(feed),
                'property_name': fake.name(),
                'price': random.randint(10000, 100000)
            }
            collection.insert(value)

    # Property Showing Part

    def get(self):
        total_collection = collection.count()
        total_page = int(total_collection/48)
        output = []

    # For Showing All Properties

        if 'page' not in request.args:
            for data in collection.find():
                output.append({'id': data['id'], 'feed': data['feed'], 'property_name': data['property_name'],
                               'price': data['price']})
            return {'Properties': output}, 200

    # For Showing 48 Property Base on Page Number

        if 'page' in request.args and 'feed_ratio' not in request.args:
            page = int(request.args['page'])
            if type(page) is int:
                if (page >= 0) and (page <= 6):
                    start = collection.find().sort('id', pymongo.ASCENDING)
                    last = start[48*page]['id']
                    number = collection.find({'id': {'$gte': last}}).sort('id', pymongo.ASCENDING).limit(48)
                    output = []
                    for i in number:
                        output.append({'id': i['id'], 'feed': i['feed'], 'property_name': i['property_name'],
                                       'price': i['price']})
                    return {'Property of page': page, 'Properties': output}
                else:
                    return {'Error': 'Enter a value of page greater than or equal 0 and less than or equal '
                                     + str(total_page)}
            else:
                return {'Error': 'Enter a Integer value of page'}, 200

    # Feed Ratio Part
        feed_ratio = request.args['feed_ratio']
        feed_ratio = ast.literal_eval(feed_ratio)
        page = int(request.args['page'])

        output = []
        feed_11 = 0
        feed_count_11 = 0
        feed_12 = 0
        feed_count_12 = 0
        feed_16 = 0
        feed_count_16 = 0

        if (page >= 0) and (page <= total_page):
            for x in feed_ratio:
                if x['feed'] == 11:
                    feed_11 = x['ratio']
                if x['feed'] == 12:
                    feed_12 = x['ratio']
                if x['feed'] == 16:
                    feed_16 = x['ratio']

            feed_ratio_1 = collection.find().sort('id', pymongo.ASCENDING).limit(299)
            for x in feed_ratio_1:
                if x['feed'] == 11:
                    feed_count_11 = feed_count_11 + 1
                if x['feed'] == 12:
                    feed_count_12 = feed_count_12 + 1
                if x['feed'] == 16:
                    feed_count_16 = feed_count_16 + 1

            last_feed11_id = page * feed_11
            last_feed12_id = page * feed_12
            last_feed16_id = page * feed_16

            feed_list_11 = collection.find({'feed': 11}).sort('id', pymongo.ASCENDING)
            feed_list_12 = collection.find({'feed': 12}).sort('id', pymongo.ASCENDING)
            feed_list_16 = collection.find({'feed': 16}).sort('id', pymongo.ASCENDING)

            last_position_11 = feed_list_11[last_feed11_id]['id']
            last_position_12 = feed_list_12[last_feed11_id]['id']
            last_position_16 = feed_list_16[last_feed11_id]['id']

            if feed_list_11.count() >= last_feed11_id:
                remain_list_11 = feed_list_11.count() - last_feed11_id
                if remain_list_11 >= feed_11:
                    feed_11_ratio = collection.find({'feed': 11, 'id': {'$gte': last_position_11}})\
                        .sort('id', pymongo.ASCENDING).limit(feed_11)
                else:
                    feed_remain_11 = feed_11 - remain_list_11
                    feed_11_ratio = collection.find({'feed': 11, 'id': {'$gte': last_position_11}})\
                        .sort('id', pymongo.ASCENDING).limit(feed_11 - feed_remain_11)
            else:
                feed_11_ratio = 0

            if feed_list_12.count() >= last_feed12_id:
                remain_list_12 = feed_list_12.count() - last_feed12_id
                if remain_list_12 >= feed_12:
                    feed_12_ratio = collection.find({'feed': 12, 'id': {'$gte': last_position_12}})\
                        .sort('id', pymongo.ASCENDING).limit(feed_12)
                else:
                    feed_remain_12 = feed_12 - remain_list_12
                    feed_12_ratio = collection.find({'feed': 12, 'id': {'$gte': last_position_12}})\
                        .sort('id', pymongo.ASCENDING).limit(feed_12 - feed_remain_12)
            else:
                feed_12_ratio = 0

            if feed_list_16.count() >= last_feed16_id:
                remain_list_16 = feed_list_16.count() - last_feed16_id
                if remain_list_16 >= feed_16:
                    feed_16_ratio = collection.find({'feed': 16, 'id': {'$gte': last_position_16}})\
                        .sort('id', pymongo.ASCENDING).limit(feed_16)
                else:
                    feed_remain_16 = feed_12 - remain_list_16
                    feed_16_ratio = collection.find({'feed': 16, 'id': {'$gte': last_position_16}})\
                        .sort('id', pymongo.ASCENDING).limit(feed_16 - feed_remain_16)
            else:
                feed_16_ratio = 0

            if feed_11_ratio:
                for x in feed_11_ratio:
                    output.append({'id': x['id'], 'feed': x['feed'], 'property_name': x['property_name'],
                                   'price': x['price']})
            if feed_12_ratio:
                for x in feed_12_ratio:
                    output.append({'id': x['id'], 'feed': x['feed'], 'property_name': x['property_name'],
                                   'price': x['price']})
            if feed_16_ratio:
                for x in feed_16_ratio:
                    output.append({'id': x['id'], 'feed': x['feed'], 'property_name': x['property_name'],
                                   'price': x['price']})
            length = len(output)
            if length <= 48:
                return {'Properties': output}
            else:
                return {'Error': 'Total Property Request Should Be Less Than 48'}
        else:
            return {'Error': 'Enter a value of page greater than or equal 0 and less than or equal ' + str(total_page)}
