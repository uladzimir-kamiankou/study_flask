from flask_restful import Resource
from models.store import StoreModel

NAME_EXISTS_ERROR = "A store with name '{}' already exists."
NOT_FOUND_ERROR = "Store not found."
INSERT_ERROR = "An error occurred while creating the store."
ITEM_DELETED_MESSAGE = "Store deleted."

class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": NOT_FOUND_ERROR}, 404

    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return (
                {"message": NAME_EXISTS_ERROR.format(name)},
                400,
            )

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": INSERT_ERROR}, 500

        return store.json(), 201

    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": ITEM_DELETED_MESSAGE}


class StoreList(Resource):
    def get(self):
        return {"stores": [x.json() for x in StoreModel.find_all()]}
