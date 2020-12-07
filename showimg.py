import matplotlib.pyplot as plt
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread(os.path.join(__location__,'out.png'))
imgplot = plt.imshow(img)
plt.show()