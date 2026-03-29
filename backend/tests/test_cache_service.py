"""
Module 2 — Cache Service
TC-F2.2: Caching behaviour
"""
import time
import pytest
from unittest.mock import patch
from app.services import cache_service


@pytest.fixture(autouse=True)
def clear_cache():
    cache_service._store.clear()
    yield
    cache_service._store.clear()


class TestCacheService:
    def test_set_and_get_returns_data(self):
        """Cache stores and retrieves data correctly."""
        cache_service.set("key1", {"data": 123})
        result = cache_service.get("key1")
        assert result == {"data": 123}

    def test_get_missing_key_returns_none(self):
        """Cache miss returns None."""
        assert cache_service.get("nonexistent") is None

    def test_invalidate_removes_entry(self):
        """TC-F2.2 — Invalidated key returns None on next get."""
        cache_service.set("key2", "value")
        cache_service.invalidate("key2")
        assert cache_service.get("key2") is None

    def test_invalidate_nonexistent_key_no_error(self):
        """Invalidating a missing key does not raise."""
        cache_service.invalidate("does_not_exist")  # should not raise

    def test_cache_age_returns_seconds(self):
        """cache_age_seconds returns a non-negative float after setting."""
        cache_service.set("key3", "data")
        age = cache_service.cache_age_seconds("key3")
        assert age is not None
        assert age >= 0

    def test_cache_age_missing_key_returns_none(self):
        assert cache_service.cache_age_seconds("missing") is None

    def test_ttl_expiry_returns_none(self):
        """TC-F2.2-02 — Expired entry returns None (past TTL)."""
        cache_service.set("key4", "stale_data")
        # Mock time so the entry looks 999 seconds old (beyond any TTL)
        with patch("app.services.cache_service.time") as mock_time:
            mock_time.time.return_value = time.time() + 9999
            result = cache_service.get("key4")
        assert result is None

    def test_within_ttl_returns_data(self):
        """TC-F2.2-01 — Entry within TTL is returned from cache."""
        cache_service.set("key5", "fresh_data")
        result = cache_service.get("key5")
        assert result == "fresh_data"

    def test_overwrite_updates_value(self):
        """Setting same key twice updates the value."""
        cache_service.set("key6", "v1")
        cache_service.set("key6", "v2")
        assert cache_service.get("key6") == "v2"
