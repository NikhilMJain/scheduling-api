from core.app.api.v1.tests.base_test_case import BaseTestCase


class TestMeetings(BaseTestCase):
    def test_create_new_meeting_for_non_existing_slot(self):
        payload = {
            "slot_id": 3,
            "subject": "Very important meeting",
            "notes": "Current pending items",
            "guest_email_ids": ['random@gmail.com']
        }
        response = self.client.post('/v1/meetings/', json=payload, headers=self.get_auth_header(1))
        self.assertEqual(response.status_code, 404)

    def test_create_new_meeting_for_existing_slot(self):
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
        second_user_header = self.get_auth_header(2)
        get_all_slots_response = self.client.get('/v1/users/{}/slots/'.format(first_user_header['user_id']),
                                   headers=second_user_header)

        meeting_payload = {
            "slot_id": get_all_slots_response.json()[0]['slot_id'],
            "subject": "Very important meeting",
            "notes": "Current pending items",
            "guest_email_ids": [
                'random@email.com'
            ]
        }
        response = self.client.post('/v1/meetings/', json=meeting_payload, headers=second_user_header)
        self.assertEqual(response.status_code, 201)
