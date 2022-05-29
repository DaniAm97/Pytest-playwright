import json
import os
import requests
from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext


@pytest.fixture(scope="session")
def api_request_context(
        playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        # We set this header per GitHub guidelines.
        "Accept": "application/vnd.github.v3+json",
        # Add authorization token to all requests.
        # Assuming personal access token available in the environment.
        # "Authorization": f"bearer {TOKEN}"

    }
    request_context = playwright.request.new_context(
        base_url="https://api-dev.hauto.dev/", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


ws_id = '6b952c5d-7fd4-4a89-b9d0-e31f29338316'


def test_create_workspace(api_request_context: APIRequestContext) -> None:
    # Login #

    data_login = {
        "email": "hobeben160@angeleslid.com",
        "password": "123456",
        "org_id": "5edfd39d-d9cd-43dc-ab36-748a03aed01d"
    }

    response = api_request_context.post(f"/api/v1/login", data=data_login)

    assert response.ok

    bearer = response.json()['access_token']
    print('Bearer', bearer)

    # Create workspace #

    data_workspace = {
        "name": "dani",
        "org_id": "5edfd39d-d9cd-43dc-ab36-748a03aed01d",
        "type": "recruiting",
        "is_collaboration": False,
        "members": [],
        "topics": []
    }
    ws_id = '6b952c5d-7fd4-4a89-b9d0-e31f29338316'

    response = api_request_context.post(f"/api/v1/workspaces/", headers={"Authorization": f"bearer {bearer}"},
                                        data=data_workspace)
    print('Response:', response.json())

    assert response.status == 201

    # Create Topic #
    data_topic = {

        "name": "123456"
    }

    response = api_request_context.post(f"/api/v1/workspaces/{ws_id}/topics/",
                                        headers={"Authorization": f"bearer {bearer}"}, data=data_topic)
    topic_id = response.json()['id']
    print('Respones topic:', response.json())

    assert response.status == 201

    # Create Skill #

    data_skill = {
        "name": "skill",
        "workspace_id": f'{ws_id}',
        "topic_id": f"{topic_id}",

    }

    response = api_request_context.post(f"api/v1/skills/", headers={
        "Authorization": f"bearer {bearer}",
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate",
        # "Content-Length": "0",
        # "Content-Type": "text/html; charset=UTF-8",
    }, data=data_skill)

    skill_id = response.json()['id']
    print('Respones skill:', response.json())

    assert response.status == 201

    # Create Step #
    data_step = {
        "name": "string",
        "display_mode": "progress",
        "widgets": [
            {
                "widget_type": 1,
                "description": "",
                "is_required": False,
                "is_gradeable": False,
                "content": {
                    "source": 101,
                    "type": 1,
                    "data": "string",
                    "data_id": "6d9132b6-7d4b-48aa-b5c7-f341d7b86bfb",
                    "description": "",
                    "options": {
                        "start_at_timestamp": "00:00",
                        "media_duration": 0
                    }
                }
            }
        ],
        "is_shared": False
    }

    response = api_request_context.post(f"/api/v1/skills/{skill_id}/steps/",
                                        headers={"Authorization": f"bearer {bearer}"}, data=data_step)
    step_id = response.json()["id"]
    print('Respones step :', response.json())
    assert response.status == 201

    # Create widget
    data_widget = {
        "widget_type": 1,
        "description": "",
        "is_required": False,
        "is_gradeable": False,
        "content": {
            "source": 101,
            "type": 1,
            "data": "string",
            "data_id": "6d9132b6-7d4b-48aa-b5c7-f341d7b86bfb",
            "description": "",
            "options": {
                "start_at_timestamp": "00:00",
                "media_duration": 0
            }
        }
    }

    response = api_request_context.post(f"/api/v1/skills/{skill_id}/steps/{step_id}/widgets/",
                                        headers={"Authorization": f"bearer {bearer}"}, data=data_widget)
    print("Respones widget :", response.json())
    assert response.status == 201
