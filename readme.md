# Image Dataset Creator 

This [script](./im_db_creator.py) create an key-value store dataset using LMDB ((Lightning Memory-Mapped Database)[https://en.wikipedia.org/wiki/Lightning_Memory-Mapped_Database]) 

## Usage:
```
$ python3 im_db_creator.py --help 
usage: im_db_creator.py [-h] [--output_folder OUTPUT_FOLDER] [--channels CHANNELS] [--width WIDTH] [--height HEIGHT] [--shuffle SHUFFLE] [--swap_channels SWAP_CHANNELS]
                        input_file

Create an LMDB dataset from existing tagged images

positional arguments:
  input_file            Input file (line: image_path label_1 label_2 ... label_n)

optional arguments:
  -h, --help            show this help message and exit
  --output_folder OUTPUT_FOLDER
                        Output dataset folder
  --channels CHANNELS   Number of channels of the input images (1-GRAY 3-RBG)
  --width WIDTH         Input image width
  --height HEIGHT       Input image height
  --shuffle SHUFFLE     Shuffle images list before create the NumPy dataset
  --swap_channels SWAP_CHANNELS
                        Use BGR instead of RGB
```

### Example:

```
$ python im_db_creator.py /Data2TB/TELEOP_DATA/annotations.txt --channels=3 --output_folder=MyDB --shuffle=True 

Shuffle: True
No. of images: 15621
Color mode   : RGB
Width        : -1
Height       : -1
Channels     : 3
image:    417/15621
```

## How to use?

```
from ImgDB import DBReader

if __name__ == "__main__":
    import matplotlib.pyplot as plt 

    db =  DBReader("./MyDB")
    for img, label in db:
        plt.imshow(img)
        print("Label", label)
        plt.show()
        
```
