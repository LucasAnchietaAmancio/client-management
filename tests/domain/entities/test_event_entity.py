import unittest

from domain.entities.event_entity import EventEntity

class TestEventEntity(unittest.TestCase):
    def test_create_event(self):
        event = EventEntity.create(
            event_id="evt_123",
            card_id="card_456",
            client_email="lucas@email.com",
            timestamp= "2026-05-18T12:00:00Z"
        )

        self.assertEqual(event.event_id, "evt_123")
        self.assertEqual(event.card_id, "card_456")
        self.assertEqual(event.client_email.value, "lucas@email.com")
        self.assertEqual(event.timestamp, "2026-05-18T12:00:00Z")

    def test_restore_event_from_database_values(self):
        event = EventEntity.restore(
            event_id="evt_123",
            card_id="card_456",
            client_email="lucas@email.com",
            timestamp="2026-05-18T12:00:00Z"
        )

        self.assertEqual(event.event_id, "evt_123")
        self.assertEqual(event.card_id, "card_456")
        self.assertEqual(event.client_email.value, "lucas@email.com")
        self.assertEqual(event.timestamp, "2026-05-18T12:00:00Z")
