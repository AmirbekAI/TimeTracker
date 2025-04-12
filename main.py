import os
import json
import datetime
import argparse
import pickle
import subprocess
import sys
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time

#Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

#Configurations
DATA_FILE = os.path.expanduser('~/Documents/TrackIt/time_data.json')
CREDENTIALS_FILE = os.path.expanduser('~/Documents/TrackIt/credentials.json')
TOKEN_FILE = os.path.expanduser('~/Documents/TrackIt/token.pickle')
CURRENT_ACTIVITY_FILE = os.path.expanduser('~/Documents/TrackIt/.current_activity')


def notify(title, message):
    """Send a desktop notification"""
    try:
        subprocess.run(['notify-send', title, message])
    except:
        print(f"{title}: {message}")

def format_time(seconds):
    """Formatting the time from seconds to HH:MM:SS"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def load_data():
    """Load time tracking data from file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
                return data
        return {"activities": [], "time_logs": []}
    except Exception as e:
        notify("Data error", f"Error loading data {e}")
        return {"activities": [], "time_logs": []}

def save_data(data):
    """Save time tracking data to file"""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        notify("Error", f"Error saving data: {e}")

def is_tracking():
    """Check if time tracking is currently active"""
    return os.path.exists(CURRENT_ACTIVITY_FILE)

def get_current_activity():
    """Get the name and the start time of the current activity"""
    if not is_tracking():
        return None, None
    
    try:
        with open(CURRENT_ACTIVITY_FILE, 'r') as file:
            data = json.load(file)
            return data["activity"], datetime.datetime.fromisoformat(data["start_time"])
    except:
        return None, None
    
def start_tracking(activity_name):
    """Start tracking time and activity"""
    data = load_data()

    if activity_name not in data["activities"]:
        data["activities"].append(activity_name)
        save_data(data)

    current_activity = {
        "activity": activity_name,
        "start_time": datetime.datetime.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(CURRENT_ACTIVITY_FILE), exist_ok=True)
    with open(CURRENT_ACTIVITY_FILE, 'w') as file:
        json.dump(current_activity, file)

    notify("Time Tracker", f"Started tracking: {activity_name}")

def stop_tracking():
    """Stop time tracking"""
    if not is_tracking():
        notify("Time Tracker", "No time tracker to stop")
        return
    
    current_activity, start_time = get_current_activity()

    end_time = datetime.datetime.now()
    elapsed = end_time - start_time
    duration_seconds = elapsed.total_seconds()

    data = load_data()

    log_entry = {
        "activity": current_activity,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": int(duration_seconds)
    }

    data["time_logs"].append(log_entry)

    save_data(data)
    os.remove(CURRENT_ACTIVITY_FILE)

    #Format the duration nicely
    time_str = format_time(duration_seconds)

    notify("Time Tracker", f"Stopped tracking: {current_activity}\nDuration: {time_str}")

    if os.path.exists(TOKEN_FILE):
        add_to_calendar(log_entry)

def get_google_calendar_service():
    """Connect to Google Calendar API"""
    creds = None

    # Load credentials from token file
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            
    # If credentials are invalid or don't exist, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        notify("Calendar Error", f"Failed to build service: {e}")
        return None
    
def add_to_calendar(log_entry):
    """Add completed activity to Google Calendar"""
    service = get_google_calendar_service()
    if not service:
        notify("Calendar Error", "Couldn't get Google Calendar service")
        return
    
    try:
        start_time = datetime.datetime.fromisoformat(log_entry["start_time"])
        end_time = datetime.datetime.fromisoformat(log_entry["end_time"])

        calendar = service.calendars().get(calendarId='primary').execute()
        calendar_timezone = calendar.get('timeZone', 'UTC')

        event = {
            'summary': log_entry["activity"],
            'description': 'Have worked during this time interval',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': calendar_timezone
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': calendar_timezone
            }
        }

        result = service.events().insert(calendarId='primary', body=event).execute()
        notify("Time Tracker", "Activity added to Google Calendar")

    except Exception as e:
        notify("Time Tracker", f"Could not add event to Google Calendar: {e}")

def main():
    # Create a parser for getting arguments
    parser = argparse.ArgumentParser(description="Time Tracker for Ubuntu")

    subparsers = parser.add_subparsers(dest='command', help='commands')

    # Adding start command
    start_parser = subparsers.add_parser('start', help='Start time tracking')
    start_parser.add_argument('activity', help='Name of activity to track')

    subparsers.add_parser('stop', help='Stop time tracking')

    args = parser.parse_args()

    if args.command == 'start':
        if is_tracking():
            stop_tracking()

        start_tracking(args.activity)

    elif args.command == 'stop':
        stop_tracking()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
