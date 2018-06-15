import numpy as np
import PIL



def image_to_torch(path, monochrome=False):
    image = PIL.Image.open("data/" + images[8])
    if monochrome:
        image = image.convert('L')
    image_data = np.asarray(image.getdata()).reshape(image.size)

    return torch.tensor(image_data, dtype=torch.float64)
