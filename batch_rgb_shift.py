from PIL import Image
from collections import deque
import argparse
import os
import binascii
OUTPUT_FORMAT = ".jpg"
IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.bmp', 'gif', 'tiff']


def rgb_shift(image, channel='r', offset=100):
    image = image.convert('RGB')
    image.load()
    r, g, b = image.split()
    channel_dict = {'r': r, 'g': g, 'b': b}
    channel_data = channel_dict[channel].getdata()
    channel_deque = deque(channel_data)
    channel_deque.rotate(offset)
    channel_dict[channel].putdata(channel_deque)
    shifted_image = Image.merge('RGB', (r, g, b))
    return shifted_image


def get_all_images_from_the_input_dir(input_dir):
    images = []
    for file in os.listdir(input_dir):
        filepath = os.path.join(input_dir, file)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in IMAGE_FORMATS:
                img = Image.open(filepath)
                images.append(img)
    return images


def save_image(image, prefix):
    """Saves an image with a unique filename to ./output directory under the calling script"""
    random_hash = str(binascii.b2a_hex(os.urandom(15)))[2:-1]
    output_image_name = prefix + "_" + random_hash + "_" + OUTPUT_FORMAT
    output_dir = "output"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir_path = os.path.join(script_dir, output_dir)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    image_path = os.path.join(output_dir_path, output_image_name)
    print("Image saved to {0}".format(image_path))
    image.save(image_path)


def main():
    images = get_all_images_from_the_input_dir(INPUT_DIR)
    for image in images:
        file_name = image.filename.split('/')[-1].split('.')[0]
        shifted_image = rgb_shift(image, channel=CHANNEL, offset=OFFSET)
        save_image(shifted_image, prefix=file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch RGB Shift')
    parser.add_argument("-c", "--channel", dest="CHANNEL", default='r', choices=['r','g','b'], help="Channel")
    parser.add_argument("-o", "--offset", dest="OFFSET", default=100, help="RGB Offset")
    parser.add_argument("-i", "--input", dest="INPUT_DIR",
                        default="/home/stephen.salmon/Pictures/test_input/three/", help="Image Input Directory")
    try:
        args = parser.parse_args()
    except:
        print("Args Error")
        parser.print_help()
        exit(2)

    if not os.path.isdir(args.INPUT_DIR):
        print("Not a valid input directory")
        exit(2)

    INPUT_DIR = args.INPUT_DIR
    CHANNEL = args.CHANNEL
    OFFSET = args.OFFSET
    main()