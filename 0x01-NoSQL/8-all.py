#!/usr/bin/env python3
""" Module for python function list_all """


def list_all(mongo_collection):
    """ lists all documents in a collection """
    if mongo_collection is not None:
        return list(mongo_collection.find())
    return []
