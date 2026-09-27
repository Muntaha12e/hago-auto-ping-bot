from app.ping_service import PingService


def test_build_payload_contains_expected_fields():
    service = PingService(url="https://example.com", interval=5)
    payload = service.build_payload()

    assert payload["event"] == "heartbeat"
    assert payload["status"] == "alive"
    assert "room_id" in payload
    assert "timestamp" in payload


def test_ping_service_interval_is_set():
    service = PingService(url="https://example.com", interval=7)
    assert service.interval == 7
