from core.app.api.v1.tests.base_test_case import BaseTestCase


class TestSlots(BaseTestCase):
    def test_slot_creation(self):
        slot_payload = [
            {
                "date": "2020-04-05",
                "time_intervals": [
                    {
                        "start_time": "2020-04-05 17:00:00",
                        "end_time": "2020-04-06 00:00:00"
                    }
                ]
            }
        ]
        first_user_header = self.get_auth_header(1)
        define_slots_response = self.client.post('/v1/slots/', json=slot_payload, headers=first_user_header)
        self.assertEqual(define_slots_response.status_code, 201)


    def test_create_slot_with_invalid_payload(self):
        slot_payload = [
            {
                "date": "2020-04-05",
                "time_intervals": [
                    {
                        "start_time": "2020-04-05 17:00:00"
                    }
                ]
            }
        ]
        first_user_header = self.get_auth_header(1)
        define_slots_response = self.client.post('/v1/slots/', json=slot_payload, headers=first_user_header)
        self.assertEqual(define_slots_response.status_code, 422)