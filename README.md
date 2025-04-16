# Al-Hayah Real Estate Development Company - Appointment Booking App

A streamlined application for booking and managing real estate project presentation appointments.

![Al-Hayah Logo](/assets/logo.png)

## Overview

This application allows Al-Hayah Real Estate Development Company to efficiently schedule and manage presentation appointments with real estate developers. The system ensures presentations are only booked on designated days (Saturdays and Tuesdays) at a specific time slot (12:00 PM for 30 minutes).

## Features

- **Appointment Booking**: Schedule presentations on Saturdays and Tuesdays at 12:00 PM
- **Calendar View**: Visual calendar showing available dates
- **Appointment Management**: View, reschedule, and cancel appointments
- **Status Tracking**: Monitor appointment status (Confirmed, Rescheduled, Cancelled)
- **Google Sheets Integration**: Store all appointment data in Google Sheets for easy access and management
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
appointment_booking_app/
├── app.py                      # Main Streamlit application
├── sheets_integration.py       # Google Sheets integration module
├── credentials_setup.md        # Guide for setting up Google Sheets API
├── deployment_instructions.md  # Instructions for deploying the application
├── user_manual.md              # User guide for the application
├── assets/
│   ├── logo.py                 # Logo generator script
│   └── logo.png                # Generated company logo
└── requirements.txt            # Python dependencies
```

## Technology Stack

- **Frontend**: Streamlit (Python-based web application framework)
- **Backend**: Python 3.10+
- **Database**: Google Sheets (via Google Sheets API)
- **Authentication**: Google OAuth 2.0 (for Google Sheets access)
- **Deployment**: Streamlit Cloud

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Google account (for Google Sheets integration)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/al-hayah-booking-app.git
   cd al-hayah-booking-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Sheets API:
   - Follow the instructions in `credentials_setup.md` to create and configure Google Sheets API credentials
   - Place the `credentials.json` file in the root directory (for development)

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Development

### Running in Development Mode

The application can run in development mode without actual Google Sheets credentials by using dummy data stored in memory. This is useful for testing and development purposes.

To run in development mode:
```bash
streamlit run app.py
```

### Adding Sample Data

The application includes a function to create sample data for testing:

```python
from sheets_integration import SheetsIntegration

sheets = SheetsIntegration()
sheets.create_sample_data()
```

### Customization

- **Logo**: Modify the `assets/logo.py` file to customize the company logo
- **Styling**: Update the CSS styles in the `load_css()` function in `app.py`
- **Date Restrictions**: Modify the `get_available_dates()` function in `app.py` to change available days

## Deployment

For detailed deployment instructions, refer to `deployment_instructions.md`. The document covers:

1. Setting up a GitHub repository
2. Deploying to Streamlit Cloud
3. Configuring Google Sheets API credentials in production
4. Security considerations

## Usage

For detailed usage instructions, refer to `user_manual.md`. The manual covers:

1. Booking new appointments
2. Viewing existing appointments
3. Rescheduling appointments
4. Cancelling appointments
5. Troubleshooting common issues

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## Contact

For support or inquiries, please contact:
- Al-Hayah Real Estate Development Company
- Email: support@al-hayah-realestate.com
- Phone: +XX-XXXX-XXXX

---

© 2025 Al-Hayah Real Estate Development Company. All rights reserved.
