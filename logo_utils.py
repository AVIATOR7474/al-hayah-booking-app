"""
This module provides a function to get the Al-Hayah logo as a base64 encoded string.
"""

import base64
import io
from PIL import Image, ImageDraw, ImageFont

def create_logo():
    """
    Create a logo for Al-Hayah Real Estate Development Company.
    
    Returns:
        PIL.Image: Logo image object
    """
    # Create a new image with white background
    width, height = 500, 200
    background_color = (255, 255, 255)
    logo = Image.new('RGBA', (width, height), background_color)
    
    # Create a drawing context
    draw = ImageDraw.Draw(logo)
    
    # Define colors
    primary_color = (0, 128, 128)  # Teal
    secondary_color = (218, 165, 32)  # Golden
    
    # Draw a decorative building shape
    # Main building
    draw.rectangle([(150, 50), (350, 150)], fill=primary_color)
    
    # Roof
    draw.polygon([(150, 50), (250, 20), (350, 50)], fill=secondary_color)
    
    # Windows
    window_color = (173, 216, 230)  # Light blue
    window_positions = [(180, 70, 210, 90), (220, 70, 250, 90), 
                        (260, 70, 290, 90), (300, 70, 330, 90),
                        (180, 110, 210, 130), (220, 110, 250, 130), 
                        (260, 110, 290, 130), (300, 110, 330, 130)]
    
    for pos in window_positions:
        draw.rectangle(pos, fill=window_color)
    
    # Door
    draw.rectangle([(235, 110), (265, 150)], fill=secondary_color)
    
    # Use default font
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()
    
    # Add company name
    company_name = "Al-Hayah"
    company_name_width = draw.textlength(company_name, font=font_large)
    draw.text(((width - company_name_width) // 2, 160), company_name, 
              fill=primary_color, font=font_large)
    
    # Add tagline
    tagline = "Real Estate Development"
    tagline_width = draw.textlength(tagline, font=font_small)
    draw.text(((width - tagline_width) // 2, 190), tagline, 
              fill=secondary_color, font=font_small)
    
    return logo

def get_logo_as_base64():
    """
    Get the logo as a base64 encoded string for embedding in HTML/CSS.
    
    Returns:
        str: Base64 encoded logo image
    """
    logo = create_logo()
    
    # Convert PIL Image to base64
    buffered = io.BytesIO()
    logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"
