from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import pandas as pd
import os

csv_path = "names.csv"
font_path = "poppins.ttf"  
font_size = 48

delegate_data = pd.read_csv(csv_path)

template_path = "template.png"

output_folder = "certificates/"
os.makedirs(output_folder, exist_ok=True)

# adjust according to template file
y_position = 720   

try:
    font = ImageFont.truetype(font_path, font_size)
except IOError:
    font = ImageFont.load_default(font_size)

for _, row in delegate_data.iterrows():
    delegate_name = row["Name"]
    if pd.isna(delegate_name) or delegate_name.strip().lower() == "no":
        continue  

    pdf_path = os.path.join(output_folder, f"{delegate_name}_certificate.pdf")

    # skip processing if pdf already exists
    if os.path.exists(pdf_path):
        continue

    template = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(template)

    # calculate text position (horizontally centered)
    text_bbox = font.getbbox(delegate_name)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = template.size
    x_position = (image_width - text_width) / 2

    # draw onto certificate
    draw.text((x_position, y_position), delegate_name, font=font, fill="white")
    temp_image_path = os.path.join(output_folder, f"{delegate_name}_certificate.png")
    template.save(temp_image_path)

    c = canvas.Canvas(pdf_path, pagesize=(template.width, template.height))
    c.drawImage(temp_image_path, 0, 0, width=template.width, height=template.height)
    c.showPage()
    c.save()

    os.remove(temp_image_path)

output_folder