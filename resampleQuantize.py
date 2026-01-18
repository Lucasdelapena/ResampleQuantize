# Lucas de la Pena
# CS4420
# Assignment 3
# 10/10/2024

import cv2
import numpy as np
import random
import os
import argparse
from screeninfo import get_monitors

def check_args(s, d, i):
    if s < 1 or s > 2:
        print("Invalid sampling method. Please choose 1 or 2.")
        return False
    if d < 1:
        print("Invalid depth. Depth must be greater than 0.")
        return False
    if i < 1 or i > 7:
        print("Invalid intensity. Please choose a value between 1 and 7.")
        return False
    return True

# Resize the image to fit the screen
def imageResize(image, maxWidth, maxHeight):
    height, width = image.shape[:2]
    if width > maxWidth or height > maxHeight:
        aspect_ratio = width / height
        if width > maxWidth:
            newWidth = maxWidth
            newHeight = int(newWidth / aspect_ratio)
        else:
            newHeight = maxHeight
            newWidth = int(newHeight * aspect_ratio)
    else:
        newWidth, newHeight = width, height
    return newHeight, newWidth

# Downsample using pixel deletion/averaging depending on the method
def downSample(image, method):
    height, width, channels = image.shape
    newHeight = height // 2
    newWidth = width // 2
    downSampleImage = np.zeros((newHeight, newWidth, channels), np.uint8)

    for x in range(newHeight):
        for y in range(newWidth):
            for c in range(channels):
                if method == 1:  # Pixel deletion
                    downSampleImage[x, y, c] = image[2*x, 2*y, c] #ex on instructions
                elif method == 2:  # Pixel averaging
                    downSampleImage[x, y, c] = np.mean(image[2*x:2*x+2, 2*y:2*y+2, c]) #ex on instructions
    return downSampleImage, newHeight, newWidth

# Upsample using pixel replication or interpolation
def upSample(image, method):
    height, width, channels = image.shape
    newHeight = height * 2
    newWidth = width * 2
    upSampleImage = np.zeros((newHeight, newWidth, channels), np.uint8)

    for x in range(height):
        for y in range(width):
            for c in range(channels):
                if method == 1:  # Pixel replication ex in instructions
                    upSampleImage[2*x, 2*y, c] = image[x, y, c]
                    upSampleImage[2*x+1, 2*y, c] = image[x, y, c]
                    upSampleImage[2*x, 2*y+1, c] = image[x, y, c]
                    upSampleImage[2*x+1, 2*y+1, c] = image[x, y, c]
                elif method == 2:  # Interpolation ex in instructions
                    upSampleImage[2*x, 2*y, c] = image[x, y, c]
                    upSampleImage[2*x+1, 2*y, c] = (image[x, y, c] + image[min(x+1, height-1), y, c]) // 2
                    upSampleImage[2*x, 2*y+1, c] = (image[x, y, c] + image[x, min(y+1, width-1), c]) // 2
                    upSampleImage[2*x+1, 2*y+1, c] = np.mean([
                        image[x, y, c],
                        image[min(x+1, height-1), y, c],
                        image[x, min(y+1, width-1), c],
                        image[min(x+1, height-1), min(y+1, width-1), c]
                    ])
    return upSampleImage, newHeight, newWidth

# Apply intensity quantization
def intensity(image, bits):
    levels = 2 ** (8 - bits)  # Number of quantization levels
    intensityImage = ((image // levels) * levels).astype(np.uint8)
    return intensityImage

# Main function
def main():
    # Parse arguments
    parser = argparse.ArgumentParser(prog='sample')
    parser.add_argument('-s', type=int, default=1, dest='sampling_Method')
    parser.add_argument('-d', type=int, default=1, dest='depth')
    parser.add_argument('-i', type=int, default=1, dest='intensity')
    parser.add_argument('imagefile', nargs='?')
    args = parser.parse_args()

    s = args.sampling_Method
    d = args.depth
    i = args.intensity

    if not check_args(s, d, i):
        return

    # Load image
    image = cv2.imread(args.imagefile)
    if image is None:
        print("Error: Image file not found.")
        return

    # Resize image to fit the screen
    for m in get_monitors():
        maxWidth, maxHeight = m.width, m.height
    height, width = imageResize(image, maxWidth, maxHeight)
    image = cv2.resize(image, (width, height))

    # Display the original image
    windowName = "Original Image"
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, width, height)
    cv2.imshow(windowName, image)
    cv2.waitKey(0)

    # Downsample image
    downSampleImage, newHeight, newWidth = downSample(image, s)


    # Apply intensity quantization after downsampling
    for f in range(d):
        downSampleImage, newHeight, newWidth = downSample(downSampleImage, s)
        intensityImage = intensity(downSampleImage, i)
        # Display the downsampled and quantized image
        windowName = f"Depth: {d}, Intensity: {i}"
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, newWidth, newHeight)
        cv2.imshow(windowName, intensityImage)
        cv2.waitKey(0)
    
    # Upsample image
    upSampleImage, newHeight, newWidth = upSample(intensityImage, s)
    # Display the upsampled image
    windowName = f"Depth: {d}, Intensity: {i}"
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, width, height)
    cv2.imshow(windowName, upSampleImage)
    cv2.waitKey(0)
    
    # Close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
