
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from threading import Lock
import requests
from io import BytesIO


BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BACKEND_DIR, 'assets')

# Parameters for the chat image
width, height = 540, 960
background_color = "#121212"  # Lightest grey in Pillow's web-safe colors
sender_color = "#1d1d1d"
receiver_color = "#2c2c2c"
text_color = "white"
timestamp_color = "white"
date_divider_color = "orange"

action_bar_height = 80  # Height of the top bar
action_bar_color = "black"
action_bar_text_color = "white"
action_bar_text_size = 22
action_bar_padding = 10
icon_size = (40, 40)
small_icon_size = (30, 30)

text_input_bottom_bar_height = 100
text_input_bottom_bar_color = "#1d1d1d"

# Font settings
# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Replace with your font path
font_size = 16
timestamp_font_size = 12

# Load fonts
font = ImageFont.load_default().font_variant(size=font_size)
timestamp_font = ImageFont.load_default().font_variant(size=timestamp_font_size)

# Initialize image
img = Image.new("RGB", (width, height), color=background_color)
draw = ImageDraw.Draw(img)

def draw_text_input_bar(draw, img):
    # Draw the background bar
    draw.rectangle(
        [(0, height - text_input_bottom_bar_height), (width, height)],
        fill=background_color
    )
    
    # Draw rounded search bar
    search_bar_padding = 10
    search_bar_height = 45
    search_bar_y = height - (text_input_bottom_bar_height // 2) - (search_bar_height // 2)
    
    # Draw rounded rectangle for search bar
    draw.rounded_rectangle(
        [
            (search_bar_padding / 2, search_bar_y - 10),
            (width - search_bar_padding / 2, search_bar_y + search_bar_height + 10)
        ],
        radius=64, # hit em with the 64 bits
        fill=None,
        outline="#595959",
        width=2
    )
    
    # Add placeholder text
    placeholder_text = "Type something..."
    placeholder_font = ImageFont.load_default().font_variant(size=18)
    text_bbox = draw.textbbox((0, 0), placeholder_text, font=placeholder_font)
    text_height = text_bbox[3] - text_bbox[1]
    text_y = search_bar_y + (search_bar_height - text_height - search_bar_padding) // 2
    
    draw.text(
        (search_bar_padding + 64, text_y),  # Extra padding for X icon
        placeholder_text,
        fill="#808080",  # Gray color for placeholder
        font=placeholder_font
    )

    # Draw the plus icon anchored to the left
    plus_icon_path = os.path.join(ASSETS_DIR, "plus.png")
    try:
        plus_icon = Image.open(plus_icon_path)
        plus_icon.thumbnail(small_icon_size)
        plus_x = search_bar_padding + 10
        plus_y = search_bar_y + (search_bar_height - plus_icon.height) // 2
        
        if plus_icon.mode == 'RGBA':
            img.paste(plus_icon, (plus_x, plus_y), plus_icon)
        else:
            img.paste(plus_icon, (plus_x, plus_y))
        
    except Exception as e:
        print(f"❌ Error loading plus icon: {str(e)}")
        
    # Add microphone icon on right (you'll need to implement this with an actual icon)
    mic_icon_path = os.path.join(ASSETS_DIR, "mic.png")
    try:
        mic_icon = Image.open(mic_icon_path)
        mic_icon.thumbnail(small_icon_size)
        mic_x = width - search_bar_padding - mic_icon.width - 10
        mic_y = search_bar_y + (search_bar_height - mic_icon.height) // 2
        
        if mic_icon.mode == 'RGBA':
            img.paste(mic_icon, (mic_x, mic_y), mic_icon)
        else:
            img.paste(mic_icon, (mic_x, mic_y))
        
    except Exception as e:
        print(f"❌ Error loading mic icon: {str(e)}")
        
    return search_bar_y

def draw_action_bar(draw, img, name, file_name):

    draw.rectangle(
        [(0, 0), (width, action_bar_height)],
        fill=action_bar_color
    )
    
    # Back arrow
    back_icon_path = os.path.join(ASSETS_DIR, "chevron.png")
    try:
        back_icon = Image.open(back_icon_path)
        back_icon.thumbnail(icon_size)
        back_y = (action_bar_height - back_icon.height) // 2

        if back_icon.mode == 'RGBA':
            img.paste(back_icon, (action_bar_padding, back_y), back_icon)
        else:
            img.paste(back_icon, (action_bar_padding, back_y))
    except Exception as e:
        print(f"❌ Error loading back icon: {str(e)}")

    # Add the icon 
    try:
        response = requests.get(file_name, timeout=10)
        image = Image.open(BytesIO(response.content))
        image.thumbnail(icon_size)
        profile_icon_y = (action_bar_height - image.height) // 2
        profile_icon_x = action_bar_padding + icon_size[0]

        # Create a circular mask
        mask = Image.new('L', icon_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, icon_size[0], icon_size[1]), fill=255)

        output = Image.new('RGBA', icon_size)
        output.paste(image, (0, 0), mask)
        output.putalpha(mask)
        
        # Paste the icon (handles transparency if PNG)
        if image.mode == 'RGBA':
            img.paste(output, (profile_icon_x, profile_icon_y), output)
        else:
            img.paste(output, (profile_icon_x, profile_icon_y))
            
        text_start_x = profile_icon_x + icon_size[0] + action_bar_padding
        
    except Exception as e:
        print(f"❌ Error loading icon: {str(e)}")
        # Fallback: start text from the left padding if icon fails
        text_start_x = action_bar_padding
    
    # Draw phone icon
    phone_icon_path = os.path.join(ASSETS_DIR, "phone.png")
    try:
        phone_icon = Image.open(phone_icon_path)
        phone_icon.thumbnail(icon_size)
        phone_y = (action_bar_height - phone_icon.height) // 2
        phone_x = width - icon_size[0] - action_bar_padding

        if phone_icon.mode == 'RGBA':
            img.paste(phone_icon, (phone_x, phone_y), phone_icon)
        else:
            img.paste(phone_icon, (phone_x, phone_y))
    except Exception as e:
        print(f"❌ Error loading phone icon: {str(e)}")
    
    # Draw the action bar text
    text_bbox = draw.textbbox((0, 0), name, font=ImageFont.load_default().font_variant(size=action_bar_text_size))
    text_height = text_bbox[3] - text_bbox[1]
    text_y = (action_bar_height - text_height - action_bar_padding) // 2  
    
    draw.text(
        (text_start_x, text_y),
        name,
        fill=action_bar_text_color,
        font=ImageFont.load_default().font_variant(size=action_bar_text_size)
    )

# Function to draw a chat bubble
def draw_bubble(
        draw, 
        img, 
        item, 
        sender=True, 
        timestamp="", 
        status=None, 
        y_position=0, 
        name="Siri", 
        file_name="",
        search_bar_y=0
    ):
    
    # Determine bubble size
    padding = 20
    max_text_width = 400

    text = item["message"]
    wrapped_text = textwrap.fill(text, width=43)

    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    bubble_width = min(max_text_width, text_width + 20)
    bubble_height = text_height + 40

    if (y_position + bubble_height + padding) > search_bar_y:
        return y_position + bubble_height + padding, item
    
    # Set position and color
    x_position = padding if sender else width - bubble_width - padding
    bubble_color = sender_color if sender else receiver_color

    # Draw bubble
    draw.rounded_rectangle(
        (x_position, y_position, x_position + bubble_width, y_position + bubble_height), 
        radius=15, 
        fill=bubble_color
    )

    # Draw text with consistent padding
    text_padding = 10
    draw.multiline_text(
        (x_position + text_padding, y_position + text_padding), 
        wrapped_text, 
        fill=text_color, 
        font=font
    )

    timestamp_x = 0
    # Draw status icon (e.g., check mark for read status)
    if not sender:
        check_icon_path = os.path.join(ASSETS_DIR, "check.png")
        try:
            check_icon = Image.open(check_icon_path)
            check_icon.thumbnail((15, 15))
            check_icon_x = x_position + bubble_width - 20
            check_icon_y = y_position + bubble_height - 20

            if check_icon.mode == 'RGBA':
                img.paste(check_icon, (check_icon_x, check_icon_y), check_icon)
            else:
                img.paste(check_icon, (check_icon_x, check_icon_y))

            timestamp_x = check_icon_x - 52

        except Exception as e:
            print(f"❌ Error loading check icon: {str(e)}")
            timestamp_x = x_position + bubble_width - 48
    else:
        timestamp_x = x_position + bubble_width - 65
        
    # Draw timestamp
    timestamp_y = y_position + bubble_height - 20
    timestamp_position = (timestamp_x, timestamp_y)
    draw.text(
        timestamp_position, 
        timestamp, 
        fill=timestamp_color, 
        font=timestamp_font
    )

    # Return the new y_position for the next message
    return y_position + bubble_height + padding, None

def draw_conversation(conversation_data, name, file_name, page=1, images_list=None):
  if images_list is None:
    images_list = []

  current_y = action_bar_height  # Starting y position

  # Initialize single image for complete conversation
  in_img = Image.new("RGB", (width, height), color=background_color)
  in_draw = ImageDraw.Draw(in_img)

  draw_action_bar(in_draw, in_img, name, file_name)
  search_bar_y = draw_text_input_bar(in_draw, in_img)
  
  # Draw complete conversation
  for i, item in enumerate(conversation_data):
      sender = item["speaker"] == "Person 1"
      current_y, remaining_item = draw_bubble(
          in_draw,
          in_img, 
          item,
          sender=sender,
          timestamp=item["timestamp"],
          y_position=current_y,
          name=name,
          file_name=file_name,
          search_bar_y=search_bar_y
      )
        
      if remaining_item:
        images_list.append(in_img)
        start_index = max(0, i - 3)
        remaining_conversation = conversation_data[start_index:]
        return draw_conversation(
            remaining_conversation, 
            name, 
            file_name, 
            page + 1, 
            images_list
        )
         
  images_list.append(in_img)
  return images_list
