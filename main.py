from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import pandas as pd
import os
import sys

def generate_certificates(csv_path, font_path, output_folder, y_position, font_size):
    try:
        delegate_data = pd.read_csv(csv_path)
        if "Name" not in delegate_data.columns:
            raise ValueError("CSV file must contain 'Name' column.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    os.makedirs(output_folder, exist_ok=True)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font '{font_path}' not found. Using default font.")
        font = ImageFont.load_default(font_size)

    for _, row in delegate_data.iterrows():
        delegate_name = row["Name"]
        if pd.isna(delegate_name) or delegate_name.strip().lower() == "no":
            continue  

        pdf_path = os.path.join(output_folder, f"{delegate_name}_certificate.pdf")

        # skip processing if PDF already exists
        if os.path.exists(pdf_path):
            print(f"Certificate for '{delegate_name}' already exists. Skipping.")
            continue

        try:
            template = Image.open("template.png").convert("RGB")
        except Exception as e:
            print(f"Error opening template: {e}")
            continue

        draw = ImageDraw.Draw(template)

        # calculate text position (horizontally centered)
        text_bbox = font.getbbox(delegate_name)
        text_width = text_bbox[2] - text_bbox[0]
        image_width, _ = template.size
        x_position = (image_width - text_width) / 2

        # draw onto certificate
        draw.text((x_position, y_position), delegate_name, font=font, fill="white")
        temp_image_path = os.path.join(output_folder, f"{delegate_name}_certificate.png")
        template.save(temp_image_path)

        # conversion to pdf
        c = canvas.Canvas(pdf_path, pagesize=(template.width, template.height))
        c.drawImage(temp_image_path, 0, 0, width=template.width, height=template.height)
        c.showPage()
        c.save()

        os.remove(temp_image_path)

if __name__ == "__main__":
    csv_path = "names.csv"
    font_path = "poppins.ttf"
    output_folder = "certificates/"
    font_size = 48
    y_position = 720
    
    # optional command line args
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
    if len(sys.argv) > 3:
        y_position = sys.argv[3]
    if len(sys.argv) > 4:
        font_size = int(sys.argv[4])
    if len(sys.argv) > 5:
        font_path = sys.argv[5]

    generate_certificates(csv_path, font_path, output_folder, y_position, font_size)
