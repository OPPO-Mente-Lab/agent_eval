from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import os, easyocr
from toolset.utils import caching, check_func_call

TOOL_NAME = __name__.split(".")[-1]




def _perform_ocr(image_path, reader):
    # Perform OCR on the image
    result = reader.readtext(image_path, width_ths = 0.8,  decoder = 'wordbeamsearch')

    # Extract text and bounding boxes from the OCR result
    extracted_text_boxes = [(entry[0], entry[1]) for entry in result if entry[2] > 0.4]

    return extracted_text_boxes


def _get_font(image, text, width, height):

    # Default values at start
    font_size = None  # For font size
    font = None  # For object truetype with correct font size
    box = None  # For version 8.0.0
    x = 0
    y = 0

    draw = ImageDraw.Draw(image)  # Create a draw object

    # Test for different font sizes
    for size in range(1, 500):

        # Create new font
        new_font = ImageFont.load_default(size=font_size)

        # Calculate bbox for version 8.0.0
        new_box = draw.textbbox((0, 0), text, font=new_font)

        # Calculate width and height
        new_w = new_box[2] - new_box[0]  # Bottom - Top
        new_h = new_box[3] - new_box[1]  # Right - Left

        # If too big then exit with previous values
        if new_w > width or new_h > height:
            break

        # Set new current values as current values
        font_size = size
        font = new_font
        box = new_box
        w = new_w
        h = new_h

        # Calculate position (minus margins in box)
        x = (width - w) // 2 - box[0]  # Minus left margin
        y = (height - h) // 2 - box[1]  # Minus top margin

    return font, x, y


def _add_discoloration(color, strength):
    # Adjust RGB values to add discoloration
    r, g, b = color
    r = max(0, min(255, r + strength))  # Ensure RGB values are within valid range
    g = max(0, min(255, g + strength))
    b = max(0, min(255, b + strength))
    
    if r == 255 and g == 255 and b == 255:
        r, g, b = 245, 245, 245

    return (r, g, b)


def _get_background_color(image, x_min, y_min, x_max, y_max):
    # Define the margin for the edges
    margin = 10

    # Crop a small region around the edges of the bounding box
    edge_region = image.crop(
        (
            max(x_min - margin, 0),
            max(y_min - margin, 0),
            min(x_max + margin, image.width),
            min(y_max + margin, image.height),
        )
    )

    # Find the most common color in the cropped region
    edge_colors = edge_region.getcolors(edge_region.size[0] * edge_region.size[1])
    background_color = max(edge_colors, key=lambda x: x[0])[1]

    # Add a bit of discoloration to the background color
    background_color = _add_discoloration(background_color, 40)

    return background_color


def _get_text_fill_color(background_color):
    # Calculate the luminance of the background color
    luminance = (
        0.299 * background_color[0]
        + 0.587 * background_color[1]
        + 0.114 * background_color[2]
    ) / 255

    # Determine the text color based on the background luminance
    if luminance > 0.5:
        return "black"  # Use black text for light backgrounds
    else:
        return "white"  # Use white text for dark backgrounds


def _replace_text_with_translation(image_path, translated_texts, text_boxes):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()

    # Replace each text box with translated text
    for text_box, translated in zip(text_boxes, translated_texts):

        if translated is None:
            continue

        # Set initial values
        x_min, y_min = text_box[0][0][0], text_box[0][0][1]
        x_max, y_max = text_box[0][0][0], text_box[0][0][1]

        for coordinate in text_box[0]:

            x, y = coordinate

            if x < x_min:
                x_min = x
            elif x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            elif y > y_max:
                y_max = y

        # Find the most common color in the text region
        background_color = _get_background_color(image, x_min, y_min, x_max, y_max)

        # Draw a rectangle to cover the text region with the original background color
        draw.rectangle(((x_min, y_min), (x_max, y_max)), fill=background_color)

        # Calculate font size, box
        font, x, y = _get_font(image, translated, x_max - x_min, y_max - y_min)

        # Draw the translated text within the box
        draw.text(
            (x_min + x, y_min + y),
            translated,
            fill=_get_text_fill_color(background_color),
            font=font,
        )

    return image


@check_func_call("dev_tools", TOOL_NAME, "image_translation")
@caching(time_str="long term", tool_name=TOOL_NAME)
def image_translation(args): # path: str, from_lang: str, to_lang: str

    try:
        languages = ['Afrikaans', 'Albanian', 'Arabic', 'Assamese', 'Azerbaijani', 'Belarusian', 'Bengali', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Chinese (simplified)', 'Chinese (traditional)', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'French', 'German', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Kannada', 'Korean', 'Latin', 'Latvian', 'Lithuanian', 'Maithili', 'Malay', 'Maltese', 'Maori', 'Marathi', 'Mongolian', 'Nepali', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Slovak', 'Slovenian', 'Spanish', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh'] 

        easyocr_languages = {'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Assamese': 'as', 'Azerbaijani': 'az', 'Belarusian': 'be', 'Bengali': 'bn', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Chinese': 'ch_sim', 'Chinese (simplified)': 'ch_sim', 'Chinese (traditional)': 'ch_tra', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Estonian': 'et', 'French': 'fr', 'German': 'de', 'Hindi': 'hi', 'Hungarian': 'hu', 'Icelandic': 'is', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Kannada': 'kn', 'Korean': 'ko', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Maithili': 'mai', 'Malay': 'ms', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Norwegian': 'no', 'Polish': 'pl', 'Portuguese': 'pt', 'Romanian': 'ro', 'Russian': 'ru', 'Slovak': 'sk', 'Slovenian': 'sl', 'Spanish': 'es', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tjk', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy'}

        google_languages = {'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Assamese': 'as', 'Azerbaijani': 'az', 'Belarusian': 'be', 'Bengali': 'bn', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Chinese': 'zh-CN', 'Chinese (simplified)': 'zh-CN', 'Chinese (traditional)': 'zh-TW', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Estonian': 'et', 'French': 'fr', 'German': 'de', 'Hindi': 'hi', 'Hungarian': 'hu', 'Icelandic': 'is', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Kannada': 'kn', 'Korean': 'ko', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Maithili': 'mai', 'Malay': 'ms', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Norwegian': 'no', 'Polish': 'pl', 'Portuguese': 'pt', 'Romanian': 'ro', 'Russian': 'ru', 'Slovak': 'sk', 'Slovenian': 'sl', 'Spanish': 'es', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy'}

        from_lang = args['from_lang']
        to_lang = args['to_lang']

        # Initialize the OCR reader
        reader = easyocr.Reader([easyocr_languages[from_lang]], model_storage_directory = 'model')

        # Initialize the Translator
        translator = GoogleTranslator(source=google_languages[from_lang], target=google_languages[to_lang])

        # Define input and output location
        # input_folder = "/home/notebook/code/personal/80400917/tmp/test_images"
        # output_folder = "."

        input_path = args['image_path']
        if not os.path.isabs(input_path):
            input_path = os.path.join(os.environ["FILE_DIR"], input_path)
            
        if not os.path.exists(input_path):
            raise Exception(f"File not found: {input_path}")

        output_path = os.path.join(os.path.dirname(__file__), "../tool_output/")
        os.makedirs(output_path, exist_ok=True)
        name, ext = os.path.splitext(os.path.basename(input_path))
        file_name = name + '_translation' + ext
        output_path = os.path.join(output_path, file_name)

        # Extract text and location
        extracted_text_boxes = _perform_ocr(input_path, reader)

        # Translate texts
        translated_texts = []
        for text_box, text in extracted_text_boxes:
            translated_texts.append(translator.translate(text))

        # Replace text with translated text
        image = _replace_text_with_translation(input_path, translated_texts, extracted_text_boxes)

        # Save modified image
        image.save(output_path)
        return {'output_image_path': output_path, 'status': 'success'}
    except Exception as e:
        return {'error': e, 'status': 'error'}