#!/usr/bin/env python3
""" Module for pyton function insert_school """


def update_topics(mongo_collection, name, topics):
    """ function that changes all topics of a school document based on the name
    """
    query = {"name": name}
    newvalues = {"$set": {"topics": topics}}
    document = mongo_collection.update_many(query, newvalues)
