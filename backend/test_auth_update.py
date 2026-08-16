from auth_helpers.service import AuthService, UpdateUserProfile


def test_update_current_user_profile(monkeypatch):
    token_data = {"sub": "mucyo.jean.2026@gmail.com"}
    stored_user = {
        "id": "ffdf8eb5-4524-4e9a-8039-bc56ed1a5cc4",
        "fname": "mucyo",
        "lname": "jean",
        "email": "mucyo.jean.2026@gmail.com",
        "department": "Engineering",
        "created_at": "2026-08-14T12:54:24.077954Z",
    }
    updated_user = {
        "id": "ffdf8eb5-4524-4e9a-8039-bc56ed1a5cc4",
        "fname": "Mucyo",
        "lname": "Jean",
        "email": "mucyo.jean.2026@gmail.com",
        "department": "Product",
        "created_at": "2026-08-14T12:54:24.077954Z",
    }

    monkeypatch.setattr("auth_helpers.service.decode_jwt_token", lambda token: token_data)
    monkeypatch.setattr("auth_helpers.service.supabase_db.find_user_by_email", lambda email: stored_user)
    monkeypatch.setattr("auth_helpers.service.supabase_db.update_user_profile", lambda user_id, payload: updated_user)

    result = AuthService.update_current_user_profile(
        "token-value",
        UpdateUserProfile(
            first_name="Mucyo",
            last_name="Jean",
            department_name="Product",
        ),
    )

    assert result.user_id == stored_user["id"]
    assert result.first_name == "Mucyo"
    assert result.last_name == "Jean"
    assert result.department_name == "Product"
