from supabase import create_client
from .config import settings

class SupabaseDatabase:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.client = create_client(self.url, self.key)
    def find_user_by_email(self, email_address):
        try:
            response = self.client.table("users").select("*").eq("email", email_address.lower()).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None

    def insert_new_user(self, user_info):
        try:
            response = self.client.table("users").insert(user_info).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None
    
supabase_db = SupabaseDatabase()
