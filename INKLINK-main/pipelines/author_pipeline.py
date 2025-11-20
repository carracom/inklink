from bson import ObjectId

def validate_author_exists_pipeline(author_id: str) -> list:
    return [
        {"$match": {
            "_id": ObjectId(author_id)
        }},
        {"$project": {
            "id": {"$toString": "$_id"},
            "name": 1,
            "lastname": 1
        }}
    ]