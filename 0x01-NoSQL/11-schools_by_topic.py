#!/usr/bin/env python3
""" Module for python function schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """ function that returns list of schools having a specific topic """
    query = {"topics": topic}
    documents = list(mongo_collection.find(query))
    return documents
