# CPS121 Project 3
# Written: <2024.11.21> <Kaiwen> <Li>
# 
# This program allows users to apply various transformations to images and create a collage.
# The transformations include grayscale, sepia tint, edge detection, mirroring, rotation, and more.
# The final collage is saved as an image and displayed on a simple web page.
##
# Change each occurrence of "_" in the list below to be "Y" or "N" to indicate
# whether or not the given transformation is implemented in your program.
#
#   Can be done using just getPixels()
#   Y Altering colors of the image
#   Y Grayscale
#   _ Making darker or lighter
#   Y Sepia-toned
#   _ Posterized
#   Need nested loops
#   Y Mirrorizing
#   Y Edge detection
#   _ Chromakey (change background)
#   _ Blurring
#   Need nested loops and alter size or shape
#   Y Rotation
#   _ Cropping
#   _ Shifting
#   Other transformations
#   _ <description of transformation>
#   _ <description of transformation>
#   _ <description of transformation>
# ============================================================================

import GCPictureTools as pgt
import pygame as pg
import os, sys
import traceback
import math

# ============================================================================
# ================ Start making changes after this comment ===================
# ============================================================================

# ---- SUPPORTING FUNCTIONS SHOULD GO HERE ----

def createDocType():
    """Returns the DOCTYPE declaration for an HTML document."""
    return "<!DOCTYPE html>\n"

def startHTML():
    """Returns the opening HTML tag."""
    return "<html>\n"

def endHTML():
    """Returns the closing HTML tag."""
    return "</html>\n"

def createBody(text):
    """Creates the body of the HTML document with the specified content."""
    return f"<body>\n{text}</body>\n"

def createImage(src):
    """Generates an HTML image tag for the specified source file."""
    return f'<img src="{src}"/>'


def mirrorImage(picture):
    """Create a mirrored version of the image."""
    # Get the dimensions of the image
    width = picture.getWidth()
    height = picture.getHeight()
    # Loop through each row of the image
    for y in range(height):
        # Loop through the left half of the image's columns
        for x in range(width // 2):
            # Get the pixel from the right half of the image
            rightPixel = picture.getPixel(x, y)
            # Get the corresponding pixel from the left half of the image
            leftPixel = picture.getPixel(width - x - 1, y)
            # Set the color of the right pixel to match the left pixel
            rightPixel.setColor(leftPixel.getColor())
    # Return the modified picture
    return picture


def rotate90R(pic):
    """Rotates image 90 degrees to the right."""
    # Get the dimensions of the original image
    width = pic.getWidth()
    height = pic.getHeight()
    
    # Create a new canvas with swapped dimensions
    canvas = pgt.Picture(height, width)
    
    # Iterate through each pixel in the original image
    for col in range(width):
        for row in range(height):
            # Get the color of the current pixel
            color = pic.getColor(col, row)
            # Set the color in the rotated position on the canvas
            canvas.setColor(height - 1 - row, col, color)
    
    # Return the rotated canvas
    return canvas    
     
def rotate90L(pic):
    """Rotates image 90 degrees to the left."""
    # Get the dimensions of the original image
    width = pic.getWidth()
    height = pic.getHeight()
    
    # Create a new canvas with swapped dimensions
    canvas = pgt.Picture(height, width)
    
    # Iterate through each pixel in the original image
    for col in range(width):
        for row in range(height):
            # Get the color of the current pixel
            color = pic.getColor(col, row)
            # Set the color in the rotated position on the canvas
            canvas.setColor(row, width - 1 - col, color)
    
    # Return the rotated canvas
    return canvas

def rotate(pic, direction, numRotation):

    """Rotates an image multiple times in a specified direction."""
    for _ in range(numRotation):
        if direction == 'l':
            # Rotate 90 degrees to the left
            pic = rotate90L(pic)
        elif direction == 'r':
            # Rotate 90 degrees to the right
            pic = rotate90R(pic)
    return pic

def betterRotate(pic, direction, numRotation):
    """More efficient way of rotating an image multiple times in a specified direction."""
    # Calculate the effective number of rotations
    numRotation2 = numRotation % 4

    # No rotation needed if the effective rotations are zero
    if numRotation2 == 0:
        return pic
    
    # Perform one rotation
    elif numRotation2 == 1:
        if direction == 'r':
            return rotate90R(pic)
        else:  # direction == 'l'
            return rotate90L(pic)
    
    # Perform two rotations
    elif numRotation2 == 2:
        if direction == 'r':
            return rotate(pic, 'r', 2)
        else:  # direction == 'l'
            return rotate(pic, 'l', 2)
    
    # Perform three rotations
    elif numRotation2 == 3:
        if direction == 'r':
            return rotate(pic, 'r', 3)
        else:  # direction == 'l'
            return rotate(pic, 'l', 3)

def grayScale(picture):
    """Converts an image to grayscale."""
    # Loop through each column (x-coordinate) of the image
    for x in range(picture.getWidth()):
        # Loop through each row (y-coordinate) of the image
        for y in range(picture.getHeight()):
            # Calculate the average of the red, green, and blue components
            value = (picture.getRed(x, y) + picture.getGreen(x, y) + picture.getBlue(x, y)) / 3
            
            # Set each color component (red, green, and blue) to the grayscale value
            picture.setRed(x, y, value)
            picture.setGreen(x, y, value)
            picture.setBlue(x, y, value)
    
    # Return the modified picture
    return picture

def sepiaTint(picture):
    """
    Applies a sepia tint to an image, giving it an "old-timey" look.
    Requires the image to be converted to grayscale first.
    """
    # Convert the image to grayscale to provide a base for the sepia effect
    grayScale(picture)
    # Loop through each column (x-coordinate) of the image
    for x in range(picture.getWidth()):
        # Loop through each row (y-coordinate) of the image
        for y in range(picture.getHeight()):
            # Get the red and blue components of the current pixel
            red = picture.getRed(x, y)
            blue = picture.getBlue(x, y)
            # Apply sepia adjustments based on the intensity of the red component
            if red < 63:  # For dark pixels
                red *= 1.1  # Slightly increase the red component
                blue *= 0.9  # Slightly decrease the blue component
            elif 63 <= red < 192:  # For mid-tone pixels
                red *= 1.15  # Moderately increase the red component
                blue *= 0.85  # Moderately decrease the blue component
            else:  # For bright pixels
                red = min(red * 1.08, 255)  # Increase red slightly, capping at 255
                blue *= 0.93  # Slightly decrease the blue component
            # Update the blue and red components of the pixel
            picture.setBlue(x, y, blue)
            picture.setRed(x, y, red)
    # Return the modified picture with the sepia tint applied
    return picture

def lineDetect(canvas):
    """
    Performs basic edge detection on an image.
    Highlights areas with significant changes in brightness.
    """
    # Create a new blank picture with the same dimensions as the original
    makeBw = pgt.Picture(canvas)
    # Iterate through all pixels except for the last row and column
    for x in range(canvas.getWidth() - 1):
        for y in range(canvas.getHeight() - 1):
            # Get the current pixel and its neighbors (down and right)
            here = canvas.getPixel(x, y)
            down = canvas.getPixel(x, y + 1)
            right = canvas.getPixel(x + 1, y)
            
            # Calculate the luminance (brightness) of each pixel
            hereLum = (here.getRed() + here.getGreen() + here.getBlue()) / 3
            downLum = (down.getRed() + down.getGreen() + down.getBlue()) / 3
            rightLum = (right.getRed() + right.getGreen() + right.getBlue()) / 3
            # Detect edges: significant luminance changes in both directions
            if abs(hereLum - downLum) > 10 and abs(hereLum - rightLum) > 10:
                # Mark the pixel as black if an edge is detected
                makeBw.setColor(x, y, 'black')
            else:
                # Mark the pixel as white if no edge is detected
                makeBw.setColor(x, y, 'white')
    
    # Return the edge-detected picture
    return makeBw

def blueIt(pic):
    """Enhances the blue tones in an image."""
    # Get the dimensions of the image
    height = pic.getHeight()
    width = pic.getWidth()
    # Loop through every pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the red, green, and blue components of the current pixel
            red = pic.getRed(x, y)
            green = pic.getGreen(x, y)
            blue = pic.getBlue(x, y)
            # Check if blue is significantly stronger than red and green
            if blue > green - 50 and blue > red - 50:
                # Set the blue component to the maximum value (255)
                pic.setColor(x, y, (red, green, 255))
    
    # Return the modified picture
    return pic

def mystery1(picture):
    """
    Applies a custom transformation that inverts brightness.
    Dark areas become bright and vice versa.
    """
    # Loop through every pixel in the image
    for x in range(picture.getWidth()):
        for y in range(picture.getHeight()):
            # Calculate the perceived brightness using weighted RGB components
            newRed = picture.getRed(x, y) * 0.299
            newGreen = picture.getGreen(x, y) * 0.587
            newBlue = picture.getBlue(x, y) * 0.114
            # Calculate the inverted brightness value
            color = 255 - (newRed + newGreen + newBlue)
            # Set the pixel color to the inverted brightness in grayscale
            picture.setColor(x, y, (color, color, color))
    # Return the transformed picture
    return picture

# ---- COLLAGE CREATION ----

def createCollage():
    """
    Creates a collage using various transformations on images.
    Returns the final collage image.
    """
    # Create a blank canvas for the collage with specified dimensions
    collage = pgt.Picture(530, 650)

    # Load input images
    pic = pgt.Picture('1122.jpg')
    pic1 = pgt.Picture('cherry.jpg')
    pics = pgt.Picture('sleep.jpg')
    picz = pgt.Picture('zuo.jpg')
    picg = pgt.Picture('guai.jpg')
    pict = pgt.Picture('three.jpg')
    pica = pgt.Picture('tang.jpg')

    # Apply transformations and copy them into the collage at specified positions
    # Convert an image to grayscale and copy it to the collage
    grayscalePic = grayScale(pgt.Picture(picg))
    grayscalePic.copyInto(collage, 1, 460)  # Place at (1, 460)

    # Create a mirrored version of an image and copy it to the collage
    mirroredPic = mirrorImage(pgt.Picture(picz))
    mirroredPic.copyInto(collage, 200, 1)  # Place at (200, 1)

    # Rotate an image by 45 degrees to the right and copy it to the collage
    rotatedPic = betterRotate(pgt.Picture(pic), "r", 45)
    rotatedPic.copyInto(collage, 1, 270)  # Place at (1, 270)

    # Enhance the blue tones in an image and copy it to the collage
    greenitPic = blueIt(pgt.Picture(pica))
    greenitPic.copyInto(collage, 300, 450)  # Place at (300, 450)

    # Perform edge detection on an image and copy it to the collage
    detectPic = lineDetect(pgt.Picture(pict))
    detectPic.copyInto(collage, 1, 1)  # Place at (1, 1)

    # Apply a brightness inversion effect and copy it to the collage
    mysPic = mystery1(pgt.Picture(pic1))
    mysPic.copyInto(collage, 200, 420)  # Place at (200, 420)

    # Apply a sepia tint to an image and copy it to the collage
    sepiatintPic = sepiaTint(pgt.Picture(pics))
    sepiatintPic.copyInto(collage, 200, 250)  # Place at (200, 250)

    # Save the collage as an image file
    collage_file = "collage.jpg"
    collage.save(collage_file)
    print(f"Collage saved as {collage_file}")

    # Create an HTML webpage displaying the collage
    webpage_file = "webpage.html"
    createWebPage(collage_file, webpage_file)
    print(f"Webpage created as {webpage_file}")

    # Return the final collage
    return collage

def createWebPage(imageFile, webPageFile):
    """
    Creates a simple HTML page that displays the collage.
    """
    # Open the specified HTML file in write mode
    htmlFile = open(webPageFile, "w")

    # Write the DOCTYPE declaration to the file
    htmlFile.write(createDocType())

    # Write the opening HTML tag and the beginning of the page structure
    htmlFile.write(startHTML())

    # Create an HTML image element with the source set to the provided image file
    text = createImage(f"{imageFile}")

    # Write the body of the HTML page, embedding the image
    htmlFile.write(createBody(text))

    # Write the closing HTML tags to complete the page structure
    htmlFile.write(endHTML())

    # Close the HTML file after writing all content
    htmlFile.close()

    # Print the name of the output file for confirmation
    print("output file:", htmlFile.name)

# ---- MAIN PROGRAM ----

if __name__ == '__main__':
    """
    Main program execution starts here.
    Handles optional command-line arguments for file names.
    """
    collageFile = None
    htmlFileName = "webpage.html"  # Default name

    if len(sys.argv) > 1:
        collageFile = sys.argv[1]
    if len(sys.argv) > 2:
        htmlFile = sys.argv[2]

    # Create the collage
    collage = createCollage()

    try:
        # Display or save the collage
        if collageFile is None:
            collage.display()
            input('Press Enter to quit...')
        else:
            print(f'Saving collage to {collageFile}')
            collage.save(collageFile)
            createWebPage(collageFile, htmlFileName)
    except:
        print('Could not show or save picture')




