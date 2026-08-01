def workflow_payload(**kwargs):

    payload = {
        "name": "Leave Approval",
        "description": "Leave workflow",
        "region_codes": ["APAC"],
    }

    payload.update(kwargs)

    return payload