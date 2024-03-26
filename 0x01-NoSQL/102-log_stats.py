#!/usr/bin/env python3
""" module for stats about Nginx logs stored in Mongodb """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    methods = {"GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0}
    total = nginx_collection.count_documents({})
    for key in methods:
        methods[key] = nginx_collection.count_documents({'method': key})
    get_status_count = nginx_collection.count_documents(
            {'method': 'GET', 'path': '/status'})
    print(f"{total} logs")
    print("Methods:")
    for key in methods:
        print(f'\tmethod {key}: {methods[key]}')
    print(f"{get_status_count} status check")
    request_info = nginx_collection.aggregate(
            [
                {
                    '$group': {'_id': "$ip", "requests": {"$sum": 1}}
                },
                {
                    "$sort": {'requests': -1}
                },
                {
                    "$limit": 10
                }
            ]
            )
    print('IPs:')
    for request in request_info:
        print(f"\t{request.get('_id')} {request.get('requests')}")
