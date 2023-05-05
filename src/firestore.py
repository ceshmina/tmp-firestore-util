from google.cloud.firestore import Client, CollectionReference, Query


def prepare_client(project_id: str) -> Client:
    client = Client(project=project_id)
    return client


def get_entries(client: Client, month: str) -> list[dict]:
    collection_ref: CollectionReference = (client
        .collection('contents').document('diary')
        .collection('months').document(month)
        .collection('entries')
        .order_by('date', direction=Query.DESCENDING)
        .order_by('created_at', direction=Query.DESCENDING)
    )

    entries = []
    for entry in collection_ref.stream():
        entries.append({'id': entry.id, **entry.to_dict()})

    return entries


def print_entries(entries: list[dict]) -> None:
    for entry in entries:
        print(entry)


def main():
    client = prepare_client('ceshmina-shu-test')
    entries = get_entries(client, '202305')
    print_entries(entries)
