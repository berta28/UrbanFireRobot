from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def apply_thermal_colormap(image_path, output_path):
    # Open the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image_np = np.array(image)

    # Apply thermal colormap
    colormap = cm.get_cmap('inferno')
    thermal_image = colormap(image_np / 255.0)  # Normalize to [0, 1]

    # Convert to 8-bit per channel
    thermal_image = (thermal_image[:, :, :3] * 255).astype(np.uint8)

    # Save the thermal image
    thermal_image_pil = Image.fromarray(thermal_image)
    thermal_image_pil.save(output_path)

def convert_to_thermal_intensity(image_path, output_path):
    # Open the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image_np = np.array(image)

    # # Normalize the intensity values to the range [0, 255]
    # min_val = np.min(image_np)
    # max_val = np.max(image_np)
    # if max_val - min_val > 0:
    #     normalized_image = (255 * (image_np - min_val) / (max_val - min_val)).astype(np.uint8)
    # else:
    #     normalized_image = image_np

    # Save the thermal intensity image
    thermal_image_pil = Image.fromarray(image_np)
    thermal_image_pil.save(output_path)


if __name__ == "__main__":
    input_image_path = '/home/vboxuser/UrbanFireRobot/ros2_ws/src/warehouse_simulation/models/fire_generator/materials/textures/fire.png'
    output_image_path = '/home/vboxuser/UrbanFireRobot/ros2_ws/src/warehouse_simulation/models/fire_generator/materials/textures/fire_thermal.png'
    convert_to_thermal_intensity(input_image_path, output_image_path)
    print(f"Thermal texture saved to {output_image_path}")