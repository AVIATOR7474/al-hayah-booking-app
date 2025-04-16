# Deployment Instructions for Al-Hayah Appointment Booking App

This guide provides step-by-step instructions for deploying the Al-Hayah Real Estate Development Company Appointment Booking Application to GitHub and Streamlit Cloud.

## Prerequisites

Before you begin, make sure you have:

1. A GitHub account
2. A Streamlit Cloud account (can be created at [https://streamlit.io/cloud](https://streamlit.io/cloud) using your GitHub account)
3. The complete application code on your local machine
4. Google Sheets API credentials (if using actual Google Sheets integration)

## Part 1: GitHub Repository Setup

### 1. Create a New GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account
2. Click on the "+" icon in the top-right corner and select "New repository"
3. Enter a repository name (e.g., "al-hayah-booking-app")
4. Add a description (optional): "Appointment booking application for Al-Hayah Real Estate Development Company"
5. Choose "Public" or "Private" visibility as per your requirements
6. Check "Add a README file"
7. Click "Create repository"

### 2. Clone the Repository to Your Local Machine

```bash
git clone https://github.com/your-username/al-hayah-booking-app.git
cd al-hayah-booking-app
```

### 3. Prepare Your Application Files

1. Copy all application files to the cloned repository folder:
   - `app.py` (main Streamlit application)
   - `sheets_integration.py` (Google Sheets integration)
   - `assets/` directory with logo files
   - `requirements.txt` (create this file as shown below)

2. Create a `requirements.txt` file with the following content:

```
streamlit==1.44.1
gspread==6.2.0
oauth2client==4.1.3
pandas==2.2.0
pillow==10.2.0
```

3. Create a `.gitignore` file to exclude sensitive information:

```
# Credentials
credentials.json
*.pem
*.key

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# OS specific
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

### 4. Commit and Push Your Code to GitHub

```bash
git add .
git commit -m "Initial commit: Al-Hayah Appointment Booking App"
git push origin main
```

## Part 2: Streamlit Cloud Deployment

### 1. Log in to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account

### 2. Deploy Your Application

1. Click on "New app" button
2. In the deployment form:
   - Select your repository (`your-username/al-hayah-booking-app`)
   - Select the branch (`main`)
   - Set the main file path to `app.py`
   - Give your app a name (e.g., "Al-Hayah-Booking")
3. Click "Deploy"

### 3. Configure Secrets for Google Sheets API (if using)

1. Once your app is deployed, go to the app settings (⋮ menu > Settings)
2. Click on "Secrets"
3. Add your Google Sheets API credentials in JSON format:

```
{
  "gcp_service_account": {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "your-private-key",
    "client_email": "your-client-email",
    "client_id": "your-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "your-cert-url"
  }
}
```

4. Click "Save"

### 4. Update Your Code to Use Streamlit Secrets (if using Google Sheets)

In your production code, you'll need to modify the `sheets_integration.py` file to use Streamlit secrets instead of a local credentials file. Add the following code to your application:

```python
import streamlit as st
import json
import tempfile

# Check if running on Streamlit Cloud with secrets
if 'gcp_service_account' in st.secrets:
    # Create a temporary file to store the credentials
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(st.secrets['gcp_service_account'], f)
        credentials_path = f.name
else:
    # Local development with credentials.json file
    credentials_path = 'credentials.json' if os.path.exists('credentials.json') else None
    
# Initialize the SheetsIntegration with the credentials path
sheets = SheetsIntegration(credentials_path)
```

### 5. Redeployment After Changes

If you make changes to your code:

1. Commit and push changes to GitHub:
```bash
git add .
git commit -m "Update application code"
git push origin main
```

2. Streamlit Cloud will automatically detect changes and redeploy your application

## Part 3: Accessing Your Deployed Application

Once deployed, your application will be available at:
```
https://al-hayah-booking-your-username.streamlit.app
```

Share this URL with the Al-Hayah Real Estate Development Company staff to start using the application.

## Troubleshooting

### Common Issues and Solutions

1. **Application Error on Streamlit Cloud**
   - Check the logs in the Streamlit Cloud dashboard
   - Verify that all required packages are in `requirements.txt`
   - Ensure your code doesn't reference local file paths

2. **Google Sheets Integration Not Working**
   - Verify that the service account has access to the Google Sheet
   - Check that the secrets are correctly configured in Streamlit Cloud
   - Ensure the Google Sheet name matches what's in your code

3. **Logo Not Displaying**
   - Make sure the logo file is included in your GitHub repository
   - Check that the path to the logo file is correct in your code

### Getting Help

If you encounter issues not covered here:
- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Visit the [Streamlit community forum](https://discuss.streamlit.io/)
- Review the [Google Sheets API documentation](https://developers.google.com/sheets/api)

## Security Considerations

1. Never commit credentials or API keys to GitHub
2. Use Streamlit secrets for storing sensitive information
3. Consider setting up IP restrictions for your Google Cloud project
4. Regularly rotate service account keys
5. Use a private GitHub repository if the application contains sensitive business logic
