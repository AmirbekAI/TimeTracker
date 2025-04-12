# Setting Up Keyboard Shortcuts for Time Tracker

This guide will help you set up keyboard shortcuts to control your Time Tracker application.

## Prerequisites

Make sure all the script files are executable:
```
chmod +x start_work.sh start_break.sh stop_tracking.sh show_status.sh
```

## Setting Up Keyboard Shortcuts in Ubuntu

1. Open the Ubuntu Settings application
2. Navigate to "Keyboard" > "Keyboard Shortcuts" > "Custom Shortcuts"
3. Click on the "+" button to add a new shortcut

### Shortcut 1: Start Work Tracking

1. Name: "Start Work Tracking"
2. Command: `/pathToTheProject/TrackIt/start_work.sh` (choose your own file location)
3. Shortcut: Choose a combination like `Ctrl+Alt+W`

### Shortcut 2: Stop Tracking

1. Name: "Stop Time Tracking"
2. Command: `pathToYourProject/TimeTracker/stop_tracking.sh`
3. Shortcut: Choose a combination like `Ctrl+Alt+S`




## Adding More Activities

To add more tracking activities, you can create additional scripts:

1. Create a new file like `start_meeting.sh` with this content:
   ```bash
   #!/bin/bash
   cd ~/Documents/TimeTracker
   source timeTrackVenv/bin/activate
   python simple_time_tracker.py start "Meeting"
   ```

2. Make it executable:
   ```
   chmod +x start_meeting.sh
   ```

3. Set up a keyboard shortcut as described above.


-------------------------------------------------------------------------------------------------------------------------

📱 Setting Up Shortcuts on Your iPhone
If you'd like to use this tool from your iPhone, you can create Shortcuts that run your tracking scripts via SSH. Here’s how to set it up:

✅ Step 1: Enable SSH on Your Linux Machine
Make sure SSH is enabled and accessible on your Linux machine. If you haven’t already, set it up and confirm you can connect via SSH.

📲 Step 2: Create a Shortcut on iPhone
Open the Shortcuts app on your iPhone.

Tap + to create a new shortcut.

Select Add Action → Scripting → Run Script over SSH.

Fill in the required SSH details:

Host: Your Linux machine’s IP address

Username and Password: Your Linux credentials

In the Script field, enter the path to your start script, e.g.:

/path/to/your/project/TrackIt/start_tracker.sh
Save the shortcut and give it a name like Start Tracking.

⏹ Create a Stop Shortcut
Repeat the same process, but for stopping the timer:

/path/to/your/project/TrackIt/stop_tracker.sh
Name the shortcut something like Stop Tracking.

🏠 Optional: Add to Home Screen
For quick access, tap the three-dot menu on each shortcut and select Add to Home Screen.

Now, with a single tap on your iPhone, you can start or stop tracking your work time—straight from your phone!