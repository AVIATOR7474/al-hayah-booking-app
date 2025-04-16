# Google Sheets API Credentials Setup Guide

This guide explains how to set up Google Sheets API credentials for the Al-Hayah Real Estate Development Company Appointment Booking App.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Steps to Create Google Sheets API Credentials

1. **Create a Google Cloud Project**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Click on the project dropdown at the top of the page
   - Click "New Project"
   - Enter a name for your project (e.g., "Al-Hayah Booking App")
   - Click "Create"

2. **Enable the Google Sheets API**
   - In the Google Cloud Console, select your project
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click on "Google Sheets API"
   - Click "Enable"

3. **Enable the Google Drive API**
   - Return to the API Library
   - Search for "Google Drive API"
   - Click on "Google Drive API"
   - Click "Enable"

4. **Create Service Account Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Enter a name for the service account (e.g., "al-hayah-booking-app")
   - Click "Create and Continue"
   - For the role, select "Project" > "Editor"
   - Click "Continue"
   - Click "Done"

5. **Generate a JSON Key File**
   - In the Credentials page, click on the service account you just created
   - Go to the "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select "JSON" as the key type
   - Click "Create"
   - The JSON key file will be downloaded to your computer

6. **Create a Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com/)
   - Create a new spreadsheet named "Al-Hayah Appointment Bookings"
   - Share the spreadsheet with the service account email (found in the JSON key file under `client_email`)
   - Give the service account "Editor" permissions

7. **Add the Credentials to the Application**
   - Rename the downloaded JSON key file to `credentials.json`
   - Place the file in the root directory of the application
   - Update the `credentials_path` parameter in the application code to point to this file

## Security Considerations

- Keep your credentials.json file secure and never commit it to public repositories
- Consider using environment variables or a secure vault for production deployments
- Regularly rotate your service account keys for enhanced security

## Troubleshooting

If you encounter issues with the Google Sheets integration:

1. Verify that the APIs are enabled for your project
2. Ensure the service account has the correct permissions on the spreadsheet
3. Check that the credentials.json file is in the correct location
4. Verify that the spreadsheet name in the code matches the actual spreadsheet name

For development purposes, the application can run without actual credentials by using dummy data stored in memory.
