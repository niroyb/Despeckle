import Image
import ImageFilter
from numpy import median

'''Filter that remove grain noise from an Image
Requires PIL and NumPy'''

IMG_IN  = r"test.png"
MAX_LUM = 220
WHITE = (255, 255, 255)

def luminosity(rgb, rcoeff=0.2126, gcoeff=0.7152, bcoeff=0.0722):
    return rcoeff*rgb[0] + gcoeff*rgb[1] + bcoeff*rgb[2]

def is_in_range(img, c, r):
    '''returns true if pixel coordinates are within the image'''
    return c >= 0 and c < img.size[0] and r >= 0 and r < img.size[1]

def get_area(img, c, r):
    '''returns at most 3*3 pixels centered on x, y'''
    ret = []
    for i in xrange(c-1, c+2):
        for j in xrange(r-1, r+2):
            if is_in_range(img, i, j):
                ret.append(img.getpixel((i,j)))
    return ret

def median_lum_area(img, c, r):
    '''Returns the median luminosity of centered pixel area'''
    area = get_area(img, c, r)
    lums = map(luminosity, area)
    return median(lums)

def test_median(img):
    area = get_area(img, 0, 0)
    lums = map(luminosity, area)
    print area
    print lums
    print 'median', median(lums)

def despeckle(img):
    res = Image.new('RGB', img.size)
    px_map = res.load()
    width, height = img.size
    for r in xrange(height):
        for c in xrange(width):
            lum = int(median_lum_area(img, c, r))
            if lum >= MAX_LUM:
                # Make high luminance pixels completely white
                px_map[c,r] = WHITE
            else:
                # Apply grayscale luminance
                px_map[c,r] = (lum, lum, lum)
    return res

def despeckle_fast(img):
    res = img.copy() 
    # Convert to grayscale
    res = res.convert('L')
    # Apply median filter te despeckle
    res = res.filter(ImageFilter.MedianFilter)
    return res

def main():
    img = Image.open(IMG_IN)

    clean_img = despeckle_fast(img)
    clean_img.save('despeckle_fast.png')

    clean_img = despeckle(img)
    clean_img.save('despeckle_slow.png')

main()
