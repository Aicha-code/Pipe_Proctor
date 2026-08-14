try:
    from supabase import create_client
except ImportError:  # pragma: no cover - optional dependency for local API-only work
    create_client = None

from .config import settings


class SupabaseDatabase:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.client = create_client(self.url, self.key) if create_client else None

    def find_user_by_email(self, email_address):
        if self.client is None:
            return None
        try:
            response = self.client.table("users").select("*").eq("email", email_address.lower()).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None

    def insert_new_user(self, user_info):
        if self.client is None:
            return None
        try:
            response = self.client.table("users").insert(user_info).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None


supabase_db = SupabaseDatabase()
