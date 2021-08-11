import cv2
import pytesseract
import numpy as np

import urllib.request


def url_to_image(url):
    """

    Args:
        url: the url of the image you want to convert to a usable image with openCV.
        User-Agent is mandatory to avoid 403 error.

    Returns: the image

    """
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = url
    headers = {'User-Agent': user_agent, }
    request = urllib.request.Request(url, None, headers)
    resp = urllib.request.urlopen(request)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


def binary_image(url):
    """
    a binary image is an image filled with only white and black pixels. easier for OpenCV to read the text on it
    Args:
        image: the image url you want to make a binary image with

    Returns: the binary image (grayscaling + bitwise-not operation)

    """
    initial_image = url_to_image(url)
    gray_img = cv2.cvtColor(initial_image, cv2.COLOR_RGB2GRAY)
    inverted_img = cv2.bitwise_not(gray_img)
    return inverted_img


def unsharp_mask(image, kernel_size=(9, 9), sigma=1.1, amount=2.5, threshold=0):
    """
    sharpening operator which enhances edges. it makes the text nice and sharp to read it.
    more infos: https://homepages.inf.ed.ac.uk/rbf/HIPR2/unsharp.htm
    Args:
        image: the image you want to sharpen
        kernel_size: the kernel slides over the image and execute the operation
        sigma: ¯\_(ツ)_/¯
        amount:  how much darker and how much lighter the edge borders become
        threshold: low values should sharpen more

    Returns:

    """
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def scan_image(image):
    """

    Args:
        image: the image you want to scan

    Returns: a list containing each unit and its quantity

    """
    scanned_img = unsharp_mask(binary_image(image))
    results = [result for result in pytesseract.image_to_string(scanned_img).split('\n') if
               result != '' and result != '\x0c' and result != ' ']
    return results


if __name__ == '__main__':
    datas = scan_image('https://cdn.discordapp.com/attachments/872570436318273596/875009763136667719/unknown.png')
    print(datas)
