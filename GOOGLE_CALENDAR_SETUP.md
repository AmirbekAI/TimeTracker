# Google Calendar API Setup Guide

This guide will help you set up the Google Calendar API integration for the Time Tracker application.

## Steps to Create Google API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. In the sidebar, navigate to "APIs & Services" > "Library"
4. Search for "Google Calendar API" and enable it
5. Go back to "APIs & Services" > "Credentials"
6. Click "Create Credentials" and select "OAuth client ID"
7. If prompted, configure the OAuth consent screen:
   - Select "External" user type (or "Internal" if you have a Google Workspace)
   - Fill in the required application information (app name, user support email, developer contact email)
   - Add the scope `.../auth/calendar` for Google Calendar access
   - **Important:** Add your email address as a test user under "Test users"
8. Create an OAuth client ID:
   - Application type: Desktop app
   - Name: Time Tracker
9. Download the credentials file
10. Rename the downloaded file to `credentials.json`
11. Place the `credentials.json` file in the same directory as the Time Tracker application

## First Run Authentication

When you first run the Time Tracker application with Google Calendar integration:

1. A browser window will open asking you to sign in to your Google account
2. **Since the app is unverified, you will see a warning screen**:
   - Click on "Advanced" at the bottom left of the warning screen
   - Click on "Go to Time Tracker (unsafe)" link
   - This is expected for applications in development/testing mode
3. Grant the requested permissions for Google Calendar
4. The browser will show a success message and you can close it
5. The application will store the authentication token for future use

## Troubleshooting OAuth Issues

If you encounter OAuth errors:

1. **"This app isn't verified" warning**:
   - This is normal for applications in development/testing mode
   - Make sure your email is added as a test user in the Google Cloud Console
   - Click "Advanced" and then "Go to Time Tracker (unsafe)" to continue

2. **"Error 403: access_denied" message**:
   - Check that your OAuth consent screen has your email as a test user
   - Make sure the Google Calendar API is enabled
   - Try deleting any existing `token.pickle` file and restarting the application
   - Ensure you've completed the OAuth consent screen setup in Google Cloud Console

3. **Authentication fails after granting permissions**:
   - Restart the application and try again
   - Verify your internet connection
   - Check that the time and date are correct on your computer

## General Troubleshooting

- If you encounter errors with the Google Calendar integration, make sure:
  - You have properly enabled the Google Calendar API
  - The `credentials.json` file is in the correct location
  - Your Google account has access to Google Calendar
  - You have internet connectivity
  - Your account is added as a test user in Google Cloud Console

## Using Time Tracker Without Google Integration

If you cannot set up Google Calendar integration, the Time Tracker application will still work for basic time tracking. Simply disable the "Sync activities with Google Calendar" option in the Settings tab. 