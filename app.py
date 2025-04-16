"""
Al-Hayah Real Estate Development Company - Appointment Booking App

This Streamlit application allows booking presentation appointments for real estate developers.
Features include booking, rescheduling, and canceling appointments.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
import os
import sys
from PIL import Image

# Add the current directory to the path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sheets_integration import SheetsIntegration
from assets.logo import get_logo_as_base64

# Set page configuration
st.set_page_config(
    page_title="Al-Hayah Appointment Booking",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'view' not in st.session_state:
    st.session_state.view = 'calendar'  # Default view
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None
if 'edit_appointment_id' not in st.session_state:
    st.session_state.edit_appointment_id = None
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""

# Initialize Google Sheets integration
@st.cache_resource
def get_sheets_integration():
    """Get or create a cached instance of SheetsIntegration."""
    # Path to credentials file - set to None for development with dummy data
    credentials_path = None
    if os.path.exists('credentials.json'):
        credentials_path = 'credentials.json'
    
    return SheetsIntegration(credentials_path)

sheets = get_sheets_integration()

# Custom CSS for styling
def load_css():
    """Load custom CSS styles."""
    st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 1rem;
        }
        
        /* Header styling */
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            flex-direction: column;
        }
        
        /* Logo styling */
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .logo-image {
            height: 100px;
        }
        
        /* Card styling */
        .card {
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
            border-left: 5px solid #008080;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card-title {
            color: #008080;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .card-subtitle {
            color: #daa520;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }
        .card-content {
            margin-bottom: 0.5rem;
        }
        .card-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
        }
        
        /* Status badges */
        .badge {
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .badge-confirmed {
            background-color: #d4edda;
            color: #155724;
        }
        .badge-cancelled {
            background-color: #f8d7da;
            color: #721c24;
        }
        .badge-rescheduled {
            background-color: #fff3cd;
            color: #856404;
        }
        
        /* Calendar styling */
        .calendar-day {
            text-align: center;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.25rem;
            cursor: pointer;
        }
        .calendar-day-available {
            background-color: #d4edda;
            color: #155724;
        }
        .calendar-day-unavailable {
            background-color: #f8d7da;
            color: #721c24;
        }
        .calendar-day-selected {
            background-color: #008080;
            color: white;
        }
        
        /* Success message */
        .success-message {
            padding: 1rem;
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        
        /* Form styling */
        .form-container {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 4rem;
            white-space: pre-wrap;
            background-color: white;
            border-radius: 4px 4px 0 0;
            gap: 1rem;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #008080;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Display logo and header
def display_header():
    """Display the application header with logo."""
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
    
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, width=300)
    else:
        # Use base64 encoded logo as fallback
        logo_base64 = get_logo_as_base64()
        st.markdown(f"""
        <div class="logo-container">
            <img src="{logo_base64}" class="logo-image">
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #008080;'>Presentation Appointment Booking</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #daa520; font-size: 1.2rem;'>Schedule, manage, and track real estate project presentations</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# Generate available dates (only Saturdays and Tuesdays)
def get_available_dates(num_weeks=4):
    """
    Generate a list of available dates (Saturdays and Tuesdays) for the next few weeks.
    
    Args:
        num_weeks: Number of weeks to generate dates for
        
    Returns:
        list: List of date objects
    """
    today = datetime.now().date()
    dates = []
    
    # Start from today and go forward
    current_date = today
    
    # Generate dates for the specified number of weeks
    for _ in range(num_weeks * 7):  # 7 days per week
        # Check if the day is Saturday (5) or Tuesday (1)
        if current_date.weekday() == 5 or current_date.weekday() == 1:
            # Only include dates from today onwards
            if current_date >= today:
                dates.append(current_date)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return dates

# Format date for display
def format_date(date_obj, include_day=True):
    """
    Format a date object for display.
    
    Args:
        date_obj: Date object to format
        include_day: Whether to include the day name
        
    Returns:
        str: Formatted date string
    """
    if include_day:
        return date_obj.strftime("%A, %d %B %Y")
    return date_obj.strftime("%d %B %Y")

# Check if a date is available for booking
def is_date_available(date_obj):
    """
    Check if a date is available for booking.
    
    Args:
        date_obj: Date object to check
        
    Returns:
        bool: True if the date is available, False otherwise
    """
    # Convert date object to string format used in the sheet
    date_str = date_obj.strftime("%Y-%m-%d")
    
    # Check if the slot is available
    return sheets.is_slot_available(date_str, "12:00")

# Display calendar view
def display_calendar_view():
    """Display the calendar view for selecting dates."""
    st.markdown("### Select a Date for Presentation")
    st.markdown("Presentations are available on **Saturdays** and **Tuesdays** at **12:00 PM** for 30 minutes.")
    
    # Get available dates
    available_dates = get_available_dates(num_weeks=4)
    
    # Group dates by week for better display
    weeks = {}
    for date in available_dates:
        # Get the week number
        week_num = date.isocalendar()[1]
        if week_num not in weeks:
            weeks[week_num] = []
        weeks[week_num].append(date)
    
    # Display weeks
    for week_num, dates in weeks.items():
        cols = st.columns(len(dates))
        for i, date in enumerate(dates):
            # Check if the date is available
            is_available = is_date_available(date)
            
            # Check if this is the selected date
            is_selected = st.session_state.selected_date == date
            
            # Determine the CSS class
            if is_selected:
                css_class = "calendar-day calendar-day-selected"
            elif is_available:
                css_class = "calendar-day calendar-day-available"
            else:
                css_class = "calendar-day calendar-day-unavailable"
            
            # Display the date
            with cols[i]:
                day_name = date.strftime("%A")
                day_num = date.strftime("%d")
                month = date.strftime("%b")
                
                # Create a clickable date card
                if st.button(
                    f"{day_name}\n{day_num} {month}",
                    key=f"date_{date}",
                    disabled=not is_available and not is_selected,
                    use_container_width=True
                ):
                    # Update the selected date
                    if is_selected:
                        st.session_state.selected_date = None
                    else:
                        st.session_state.selected_date = date
                    
                    # Rerun the app to update the UI
                    st.rerun()

# Display booking form
def display_booking_form():
    """Display the booking form for the selected date."""
    if st.session_state.selected_date:
        st.markdown(f"### Book Presentation for {format_date(st.session_state.selected_date)}")
        st.markdown("Please fill in the details below to book your presentation slot.")
        
        # Create a form
        with st.form(key="booking_form"):
            # Company details
            company_name = st.text_input("Company Name", key="company_name")
            project_name = st.text_input("Project Name", key="project_name")
            area = st.text_input("Area/Location", key="area")
            representative = st.text_input("Developer Representative Name", key="representative")
            
            # Submit button
            submit_button = st.form_submit_button("Book Appointment")
            
            if submit_button:
                # Validate form
                if not company_name or not project_name or not area or not representative:
                    st.error("Please fill in all fields.")
                else:
                    # Format date for the sheet
                    date_str = st.session_state.selected_date.strftime("%Y-%m-%d")
                    
                    # Add the appointment
                    success = sheets.add_appointment(
                        company_name,
                        project_name,
                        area,
                        date_str,
                        "12:00",
                        representative
                    )
                    
                    if success:
                        # Show success message
                        st.session_state.show_success = True
                        st.session_state.success_message = f"Appointment booked successfully for {format_date(st.session_state.selected_date)} at 12:00 PM."
                        
                        # Reset the selected date
                        st.session_state.selected_date = None
                        
                        # Rerun the app to update the UI
                        st.rerun()
                    else:
                        st.error("Failed to book appointment. Please try again.")

# Display appointment card
def display_appointment_card(appointment):
    """
    Display an appointment card.
    
    Args:
        appointment: Dictionary containing appointment details
    """
    # Parse the date
    try:
        date_obj = datetime.strptime(appointment['Presentation Date'], "%Y-%m-%d").date()
        formatted_date = format_date(date_obj)
    except:
        formatted_date = appointment['Presentation Date']
    
    # Determine the status badge class
    status = appointment['Status']
    if status == "Confirmed":
        badge_class = "badge badge-confirmed"
    elif status == "Cancelled":
        badge_class = "badge badge-cancelled"
    else:  # Rescheduled
        badge_class = "badge badge-rescheduled"
    
    # Create the card
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{appointment['Company Name']} - {appointment['Project Name']}</div>
        <div class="card-subtitle">{appointment['Area']}</div>
        <div class="card-content">
            <p><strong>Date:</strong> {formatted_date}</p>
            <p><strong>Time:</strong> {appointment['Time']} PM</p>
            <p><strong>Representative:</strong> {appointment['Developer Representative']}</p>
        </div>
        <div class="card-footer">
            <span class="{badge_class}">{status}</span>
            <div>
                <button onclick="document.getElementById('edit_{appointment['ID']}').click()">Edit</button>
                <button onclick="document.getElementById('cancel_{appointment['ID']}').click()">Cancel</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden buttons for edit and cancel actions
    if st.button("Edit", key=f"edit_{appointment['ID']}", help="Edit this appointment", type="primary", use_container_width=True):
        st.session_state.edit_appointment_id = appointment['ID']
        st.session_state.view = 'edit'
        st.rerun()
    
    if st.button("Cancel", key=f"cancel_{appointment['ID']}", help="Cancel this appointment", type="secondary", use_container_width=True):
        # Cancel the appointment
        success = sheets.cancel_appointment(appointment['ID'])
        
        if success:
            # Show success message
            st.session_state.show_success = True
            st.session_state.success_message = f"Appointment cancelled successfully."
            
            # Rerun the app to update the UI
            st.rerun()
        else:
            st.error("Failed to cancel appointment. Please try again.")

# Display all appointments
def display_appointments():
    """Display all appointments."""
    # Get all appointments
    df = sheets.get_all_appointments()
    
    if df.empty:
        st.info("No appointments found.")
        return
    
    # Convert DataFrame to list of dictionaries
    appointments = df.to_dict('records')
    
    # Group appointments by status
    confirmed = [a for a in appointments if a['Status'] == 'Confirmed']
    rescheduled = [a for a in appointments if a['Status'] == 'Rescheduled']
    cancelled = [a for a in appointments if a['Status'] == 'Cancelled']
    
    # Display tabs for different status groups
    tab1, tab2, tab3 = st.tabs(["Confirmed", "Rescheduled", "Cancelled"])
    
    with tab1:
        if confirmed:
            for appointment in confirmed:
                display_appointment_card(appointment)
        else:
            st.info("No confirmed appointments.")
    
    with tab2:
        if rescheduled:
            for appointment in rescheduled:
                display_appointment_card(appointment)
        else:
            st.info("No rescheduled appointments.")
    
    with tab3:
        if cancelled:
            for appointment in cancelled:
                display_appointment_card(appointment)
        else:
            st.info("No cancelled appointments.")

# Display edit form
def display_edit_form():
    """Display the form for editing an appointment."""
    if st.session_state.edit_appointment_id:
        # Get the appointment details
        appointment = sheets.get_appointment_by_id(st.session_state.edit_appointment_id)
        
        if appointment:
            st.markdown(f"### Edit Appointment")
            st.markdown("Update the appointment details below.")
            
            # Create a form
            with st.form(key="edit_form"):
                # Company details
                company_name = st.text_input("Company Name", value=appointment['Company Name'], key="edit_company_name")
                project_name = st.text_input("Project Name", value=appointment['Project Name'], key="edit_project_name")
                area = st.text_input("Area/Location", value=appointment['Area'], key="edit_area")
                representative = st.text_input("Developer Representative Name", value=appointment['Developer Representative'], key="edit_representative")
                
                # Date selection
                st.markdown("### Select a New Date")
                st.markdown("Presentations are available on **Saturdays** and **Tuesdays** at **12:00 PM** for 30 minutes.")
                
                # Get available dates
                available_dates = get_available_dates(num_weeks=4)
                
                # Convert current date string to date object
                current_date = datetime.strptime(appointment['Presentation Date'], "%Y-%m-%d").date()
                
                # Add current date to available dates if not already included
                if current_date not in available_dates:
                    available_dates.append(current_date)
                    available_dates.sort()
                
                # Create a list of date strings for the selectbox
                date_options = [format_date(date) for date in available_dates]
                current_date_str = format_date(current_date)
                
                # Find the index of the current date
                current_date_index = date_options.index(current_date_str) if current_date_str in date_options else 0
                
                # Display the selectbox
                selected_date_str = st.selectbox(
                    "Select Date",
                    date_options,
                    index=current_date_index,
                    key="edit_date"
                )
                
                # Convert selected date string back to date object
                selected_date = available_dates[date_options.index(selected_date_str)]
                
                # Submit buttons
                col1, col2 = st.columns(2)
                with col1:
                    cancel_button = st.form_submit_button("Cancel", type="secondary")
                with col2:
                    submit_button = st.form_submit_button("Update Appointment")
                
                if cancel_button:
                    # Reset the edit appointment ID
                    st.session_state.edit_appointment_id = None
                    st.session_state.view = 'calendar'
                    st.rerun()
                
                if submit_button:
                    # Validate form
                    if not company_name or not project_name or not area or not representative:
                        st.error("Please fill in all fields.")
                    else:
                        # Format date for the sheet
                        date_str = selected_date.strftime("%Y-%m-%d")
                        
                        # Check if the date has changed
                        is_rescheduled = date_str != appointment['Presentation Date']
                        
                        # Update the appointment
                        success = sheets.update_appointment(
                            st.session_state.edit_appointment_id,
                            company_name=company_name,
                            project_name=project_name,
                            area=area,
                            presentation_date=date_str,
                            developer_representative=representative,
                            status="Rescheduled" if is_rescheduled else appointment['Status']
                        )
                        
                        if success:
                            # Show success message
                            st.session_state.show_success = True
                            if is_rescheduled:
                                st.session_state.success_message = f"Appointment rescheduled successfully to {format_date(selected_date)} at 12:00 PM."
                            else:
                                st.session_state.success_message = f"Appointment updated successfully."
                            
                            # Reset the edit appointment ID
                            st.session_state.edit_appointment_id = None
                            st.session_state.view = 'calendar'
                            
                            # Rerun the app to update the UI
                            st.rerun()
                        else:
                            st.error("Failed to update appointment. Please try again.")
        else:
            st.error("Appointment not found.")
            
            # Reset the edit appointment ID
            st.session_state.edit_appointment_id = None
            st.session_state.view = 'calendar'
            st.rerun()

# Main application
def main():
    """Main application function."""
    # Load custom CSS
    load_css()
    
    # Display header
    display_header()
    
    # Display success message if needed
    if st.session_state.show_success:
        st.markdown(f"""
        <div class="success-message">
            {st.session_state.success_message}
        </div>
        """, unsafe_allow_html=True)
        
        # Reset success message after displaying
        st.session_state.show_success = False
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📅 Book Appointment", "📋 View Appointments"])
    
    with tab1:
        # Calendar view
        display_calendar_view()
        
        # Booking form
        if st.session_state.selected_date:
            display_booking_form()
    
    with tab2:
        # Appointments view
        display_appointments()
    
    # Edit view (displayed outside tabs when active)
    if st.session_state.view == 'edit':
        display_edit_form()
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2025 Al-Hayah Real Estate Development Company</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
