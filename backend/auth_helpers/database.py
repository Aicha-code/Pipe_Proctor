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

    def update_user_profile(self, user_id, user_update):
        if self.client is None:
            return None
        try:
            response = (
                self.client.table("users")
                .update(user_update)
                .eq("id", user_id)
                .select("*")
                .execute()
            )
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None

    def insert_detection(self, payload):
        if self.client is None:
            return None
        try:
            response = self.client.table("detections").insert(payload).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None

    def list_detections(self, anomaly_type=None, anomaly_status=None, from_date=None, to_date=None):
        if self.client is None:
            return []
        try:
            query = self.client.table("detections").select("*")
            if anomaly_type is not None:
                query = query.eq("anomaly_type", anomaly_type)
            if anomaly_status is not None:
                query = query.eq("anomaly_status", anomaly_status)
            if from_date is not None:
                query = query.gte("detected_at", from_date.isoformat())
            if to_date is not None:
                query = query.lte("detected_at", to_date.isoformat())
            response = query.order("detected_at", desc=True).execute()
            return response.data or []
        except Exception:
            return []

    def get_detection_by_id(self, detection_id):
        if self.client is None:
            return None
        try:
            response = self.client.table("detections").select("*").eq("id", detection_id).limit(1).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None

    def delete_detection(self, detection_id):
        """Delete one detection by id. Returns True when a row was removed."""
        if self.client is None:
            return False
        try:
            response = (
                self.client.table("detections")
                .delete()
                .eq("id", detection_id)
                .execute()
            )
            return bool(response.data)
        except Exception:
            return False

    def update_detection_status(self, detection_id, anomaly_status):
        if self.client is None:
            return None
        try:
            response = (
                self.client.table("detections")
                .update({"anomaly_status": anomaly_status, "updated_at": _utc_now().isoformat()})
                .eq("id", detection_id)
                .select("*")
                .execute()
            )
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None


def _utc_now():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc)


supabase_db = SupabaseDatabase()
