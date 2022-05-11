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






data_login = {
        "email": "hobeben160@angeleslid.com",
        "password": "123456",
        "org_id": "5edfd39d-d9cd-43dc-ab36-748a03aed01d"
    }


data_workspace = {
    "name": "dani",
    "org_id": "",
    "type": "recruiting",
    "is_collaboration":False,
    "members": [],
    "topics": []
    }




def test_craete_workspace(api_request_context:APIRequestContext) -> None:

    response = api_request_context.post(f"/api/v1/login", data=data_login)

    assert response.ok

    bearer = response.json()['access_token']
    print('Bearer',bearer)

    response = api_request_context.post("/api/v1/workspaces",headers={"Authorization": f"bearer {bearer}"}, data=data_workspace)
    print('Response:',response.json())

    assert response.status == '201'


