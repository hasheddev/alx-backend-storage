#!/usr/bin/env python3
""" module for function top_students """


def top_students(mongo_collection):
    """ A  function that returns all students sorted by average score """
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "_id": "$_id"
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
        ])
