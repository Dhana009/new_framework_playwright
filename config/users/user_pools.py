"""
Role-based user pools.

Each user entry must contain:
- id        : unique identifier (string/int)
- email     : login email
- password  : login password
- role      : ADMIN | EDITOR | VIEWER

IMPORTANT:
- These are TEST USERS only
- Credentials should come from env vars or secrets in real setups
- For now, structure correctness matters more than values
"""

ADMIN_USERS = [
    {
        "id": "admin_1",
        "email": "admin1@test.com",
        "password": "Admin@123",
        "role": "ADMIN",
    },
    {
        "id": "admin_2",
        "email": "admin2@test.com",
        "password": "Admin@123",
        "role": "ADMIN",
    },
]

EDITOR_USERS = [
    {
        "id": "editor_1",
        "email": "editor1@test.com",
        "password": "Editor@123",
        "role": "EDITOR",
    },
    {
        "id": "editor_2",
        "email": "editor2@test.com",
        "password": "Editor@123",
        "role": "EDITOR",
    },
]

VIEWER_USERS = [
    {
        "id": "viewer_1",
        "email": "viewer1@test.com",
        "password": "Viewer@123",
        "role": "VIEWER",
    },
    {
        "id": "viewer_2",
        "email": "viewer2@test.com",
        "password": "Viewer@123",
        "role": "VIEWER",
    },
]
