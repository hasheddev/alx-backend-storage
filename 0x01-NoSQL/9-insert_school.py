#!/usr/bin/env python3
""" Module for pyton function insert_school """


def insert_school(mongo_collection, **kwargs):
    """ inserts a document into a collection and return its id """
    document = mongo_collection.insert_one(kwargs)
    return document.inserted_id
