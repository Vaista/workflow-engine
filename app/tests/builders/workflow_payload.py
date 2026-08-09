def create_workflow_payload(**kwargs):

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": ["APAC"],
    }

    payload.update(kwargs)

    return payload


def search_workflow_payload(**kwargs):

    payload = {
        'org_id': 1,
        'org_unit_id': None,
        'name': None,
        'region': [],
        'created_by': None,
        'order_by': [],
        'limit': 25,
        'offset': 0
    }

    payload.update(kwargs)

    return payload