import os
from PIL import Image
import numpy as np
from rembg import remove

def change_background(input_path, output_path, bg_color):
    """
    Change the background of an image to a specified color.
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save the output image
        bg_color (tuple): RGB color tuple for background (e.g., (255, 0, 0) for red)
    """
    try:
        # Open the image
        input_image = Image.open(input_path)
        
        # Remove the background
        removed_bg = remove(input_image)
        
        # Create new background image with specified color
        background = Image.new('RGBA', input_image.size, bg_color + (255,))  # Add alpha channel
        
        # Composite the foreground onto the colored background
        final_image = Image.alpha_composite(background, removed_bg)
        
        # Convert to RGB mode before saving as JPEG
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            final_image = final_image.convert('RGB')
        
        # Save the result
        final_image.save(output_path)
        print(f"Successfully saved processed image to {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Get user input
    while True:
        input_path = input("Enter the path to your image: ").strip('"')  # Strip quotes if user drags file
        if os.path.exists(input_path):
            break
        print("File does not exist. Please try again.")

    # Get color input
    print("\nChoose background color:")
    print("1. Enter RGB values")
    print("2. Use predefined color")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        # Get RGB values
        try:
            r = int(input("Enter Red value (0-255): "))
            g = int(input("Enter Green value (0-255): "))
            b = int(input("Enter Blue value (0-255): "))
            bg_color = (r, g, b)
        except ValueError:
            print("Invalid input. Using white as default.")
            bg_color = (255, 255, 255)
    else:
        # Predefined colors
        colors = {
            '1': ((255, 255, 255), 'White'),
            '2': ((0, 0, 0), 'Black'),
            '3': ((255, 0, 0), 'Red'),
            '4': ((0, 255, 0), 'Green'),
            '5': ((0, 0, 255), 'Blue'),
        }
        
        print("\nAvailable colors:")
        for key, (_, name) in colors.items():
            print(f"{key}. {name}")
        
        color_choice = input("Choose a color number: ")
        bg_color = colors.get(color_choice, ((255, 255, 255), 'White'))[0]

    # Get output path
    default_output = os.path.splitext(input_path)[0] + "_new_bg.png"
    output_path = input(f"Enter output path (press Enter for default: {default_output}): ")
    if not output_path:
        output_path = default_output

    # Process the image
    print("\nProcessing image...")
    change_background(input_path, output_path, bg_color)

if __name__ == "__main__":
    print("Welcome to Image Background Changer!")
    print("===================================")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
