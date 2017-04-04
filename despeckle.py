'''Hello'''
from PIL import Image
from PIL import ImageFilter
from numpy import median

'''Filter that remove grain noise from an Image
Requires PIL and NumPy'''

IMG_IN = r"place_s.png"
MAX_LUM = 220
WHITE = (255, 255, 255)

def luminosity(rgb, rcoeff=0.2126, gcoeff=0.7152, bcoeff=0.0722):
    '''Get luminosity of rgb pixel based on human perception'''
    return rcoeff*rgb[0] + gcoeff*rgb[1] + bcoeff*rgb[2]

def is_in_range(img, column, row):
    '''returns true if pixel coordinates are within the image'''
    return column >= 0 and column < img.size[0] and row >= 0 and row < img.size[1]

def get_area(img, column, row):
    '''returns at most 3*3 pixels centered on x, y'''
    ret = []
    for i in range(column-1, column+2):
        for j in range(row-1, row+2):
            if is_in_range(img, i, j):
                ret.append(img.getpixel((i, j)))
    return ret

def median_lum_area(img, column, row):
    '''Returns the median luminosity of centered pixel area'''
    area = get_area(img, column, row)
    lums = list(map(luminosity, area))
    return median(lums)

def test_median(img):
    area = get_area(img, 0, 0)
    lums = map(luminosity, area)
    print(area)
    print(lums)
    print('median', median(lums))

def despeckle(img):
    res = Image.new('RGB', img.size)
    px_map = res.load()
    width, height = img.size
    for row in range(height):
        for column in range(width):
            lum = int(median_lum_area(img, column, row))
            if lum >= MAX_LUM:
                # Make high luminance pixels completely white
                px_map[column, row] = WHITE
            else:
                # Apply grayscale luminance
                px_map[column, row] = (lum, lum, lum)
    return res

def intersect(img1, img2):
    assert img1.size == img2.size
    res = Image.new('RGB', img1.size)
    px_map = res.load()
    width, height = img1.size
    for row in range(height):
        if row%100 == 0:
            print(row/10)
        for column in range(width):
            color = img1.getpixel((column, row))
            if color == img2.getpixel((column, row)):
                px_map[column, row] = color
    return res


def despeckle_fast(img):
    res = img.copy()
    # Convert to grayscale
    # res = res.convert('L')
    # Apply median filter te despeckle
    res = res.filter(ImageFilter.MedianFilter(5))
    return res



def main():
    '''Main'''
    img = Image.open(IMG_IN)
    img = img.convert('RGB')

    clean_img = despeckle_fast(img)
    clean_img.save('despeckle_fast.png')

    intersect_img = intersect(img, clean_img)
    intersect_img.save('intersect.png')
    
    # clean_img = despeckle(img)
    # clean_img.save('despeckle_slow.png')

main()
