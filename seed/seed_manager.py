from seed.admin_seed import AdminSeed


class SeedManager:
    def __init__(self, api_client):
        self.admin_seed = AdminSeed(api_client)

    def ensure_seed(self, role: str):
        if role == "ADMIN":
            self.admin_seed.ensure()
