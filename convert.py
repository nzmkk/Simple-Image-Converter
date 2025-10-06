import os
from PIL import Image

SUPPORTED_EXTENSIONS = ['.png',
                        '.jpg',
                        '.jpeg',
                        '.bmp', 
                        '.tiff',
                        '.webp',
                        '.gif',
                        '.ico',
                        '.heif',
                        '.jp2',
                        '.j2k',
                        '.jpf',
                        '.pdf'
                        ]
SAVE_FOLDER = "saved"


def find_images(input_path):
    images = []
    for filename in os.listdir(input_path):
        if any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            images.append(filename)
    if len(images) <= 0:
        print("Folder is empty, error")
        return
    else:
        print("Founded images - " + str(images))

        output_extension = input("Enter the extension you want to convert the image to (example - .png): ")
        if output_extension not in SUPPORTED_EXTENSIONS:
            print("Unsupported extension...")
            return
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)
        for image_file in images:
            input_image_path = os.path.join(input_path, image_file)
            output_filename = os.path.splitext(image_file)[0] + output_extension
            output_image_path = os.path.join(SAVE_FOLDER, output_filename)
            convert_image(input_image_path, output_image_path)
        
def convert_image(input_path ,output_path):
        try:
            with Image.open(input_path) as img:
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                img.save(output_path)
                print(f"Success: Converted {input_path} to {output_path}")
                return True
        except Exception as e:
         print(f"Error converting {input_path}: {e}")
         return False
