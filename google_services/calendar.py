from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from google_services.google_api import get_calendar_service


class CalendarService:
    def __init__(self):
        self.service = get_calendar_service()

    def create_event(self, summary: str, start_time: datetime, end_time: datetime,
                     description: str = None, location: str = None, attendees: List[str] = None,
                     timezone: str = 'UTC+2') -> Dict[str, Any]:
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': timezone,
            }
        }

        if attendees:
            event['attendees'] = [{'email': attendee} for attendee in attendees]

        try:
            return self.service.events().insert(calendarId='primary', body=event).execute()
        except Exception as e:
            raise Exception(f"Failed to create event: {str(e)}")

    def get_events(self, max_results: int = 10, time_min: datetime = None,
                   time_max: datetime = None, query: str = None) -> List[Dict[str, Any]]:
        if time_min is None:
            time_min = datetime.utcnow()

        params = {
            'calendarId': 'primary',
            'maxResults': max_results,
            'timeMin': time_min.isoformat() + 'Z',
            'singleEvents': True,
            'orderBy': 'startTime'
        }

        if time_max:
            params['timeMax'] = time_max.isoformat() + 'Z'
        if query:
            params['q'] = query

        try:
            events_result = self.service.events().list(**params).execute()
            return events_result.get('items', [])
        except Exception as e:
            raise Exception(f"Failed to fetch events: {str(e)}")

    def update_event(self, event_id: str, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            event.update(updated_data)
            return self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
        except Exception as e:
            raise Exception(f"Failed to update event: {str(e)}")

    def delete_event(self, event_id: str) -> None:
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        except Exception as e:
            raise Exception(f"Failed to delete event: {str(e)}")

    def get_upcoming_events(self, days: int = 7) -> List[Dict[str, Any]]:
        time_min = datetime.utcnow()
        time_max = time_min + timedelta(days=days)
        return self.get_events(time_min=time_min, time_max=time_max)

    def quick_add_event(self, text: str) -> Dict[str, Any]:
        try:
            return self.service.events().quickAdd(
                calendarId='primary',
                text=text
            ).execute()
        except Exception as e:
            raise Exception(f"Failed to quick add event: {str(e)}")

    def get_calendar_list(self) -> List[Dict[str, Any]]:
        try:
            calendar_list = self.service.calendarList().list().execute()
            return calendar_list.get('items', [])
        except Exception as e:
            raise Exception(f"Failed to fetch calendar list: {str(e)}")
