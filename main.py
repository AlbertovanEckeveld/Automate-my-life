from ai.ai import OllamaAssistant

def main():
    assistant = OllamaAssistant()

    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        print(assistant.handle_request(query)["ai_response"])


if __name__ == "__main__":
    main()
#    calendar2 = CalendarService()
#    print(calendar2.create_event(
#        summary="Test Event",
#        start_time=datetime(2025, 5, 15, 10, 0),
#        end_time=datetime(2025, 5, 15, 11, 0),
#        description="This is a test event",
#        location="123 Test St, Test City, TX",
#        attendees=["eckeveld@outlook.com"]
#    ))
#    print(calendar2.get_events(
#        time_min=datetime(2025, 5, 15, 0, 0),
#        time_max=datetime(2025, 5, 16, 0, 0),
#        query="Test"
#    ))

#    print(calendar2.update_event(
#        event_id="3ph9vbdkbp4939f42httfvnsb4",
#        updated_data={
#            'summary': 'Updated Event',
#            'description': 'Updated description'
#        }
#    ))
#    print(calendar2.delete_event(event_id="3ph9vbdkbp4939f42httfvnsb4"))

