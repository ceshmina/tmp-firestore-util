from google.cloud.firestore import Client, CollectionReference, DELETE_FIELD, Query


def prepare_client(project_id: str) -> Client:
    client = Client(project=project_id)
    return client


def get_collection(client: Client, month: str) -> CollectionReference:
    return (client
        .collection('contents').document('diary')
        .collection('months').document(month)
        .collection('entries'))


def add_dummy_field(collection: CollectionReference) -> None:
    for document in collection.stream():
        collection.document(document.id).update({'dummy': 'dummy'})


def remove_dummy_field(collection: CollectionReference) -> None:
    for document in collection.stream():
        collection.document(document.id).update({'dummy': DELETE_FIELD})


def set_original_time(collection: CollectionReference) -> None:
    for document in collection.stream():
        collection.document(document.id).update({
            'created_at': document.create_time,
            'updated_at': document.update_time
        })


def set_date_as_id(collection: CollectionReference) -> None:
    for document in collection.stream():
        data = document.to_dict()
        collection.document(document.id).delete()
        new_document = collection.document(data['date'])
        new_document.set(data)


def set_id_as_date(collection: CollectionReference) -> None:
    for document in collection.stream():
        data = document.to_dict()
        collection.document(document.id).delete()
        new_document = collection.document(data['date'][8:])
        new_document.set(data)


def print_data(collection: CollectionReference) -> None:
    query = (collection
        .order_by('date', direction=Query.DESCENDING)
        .order_by('created_at', direction=Query.DESCENDING))

    for document in query.stream():
        data = {'id': document.id, **document.to_dict()}
        print(data)


def main():
    client = prepare_client('ceshmina-shu-test')
    collection = get_collection(client, '202305')
    # add_dummy_field(collection)
    # remove_dummy_field(collection)
    set_date_as_id(collection)
    set_id_as_date(collection)
    set_original_time(collection)
    print_data(collection)
