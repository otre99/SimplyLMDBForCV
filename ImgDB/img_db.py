from os.path import split, join, isabs, exists
from os import mkdir
from PIL import Image
import numpy as np
from io import BytesIO
import pickle
import lmdb
import argparse
import os

class DBReader:
    def __init__(self, root):

        self.db = lmdb.open(root, max_readers=32, readonly=True,
                            lock=False, readahead=False, meminit=False)

        with self.db.begin(write=False) as txn:
            self.length = txn.stat()['entries']

    def __getitem__(self, index):
        img, target = None, None
        with self.db.begin(write=False) as txn:
            key = "{}".format(index)
            pair = Deserialize(txn.get(key.encode("ascii")))
        img = pair.get_img()
        target = pair.get_label()

        return img, target

    def __len__(self):
        return self.length


class ImageLabelPairEncoder:
    def __init__(self, img: Image.Image, label: np.ndarray, enc="JPEG"):
        self.enc = enc
        self.lb_shape = label.shape
        self.lb_dtype = label.dtype
        self.label = label.tobytes()

        buffer = BytesIO()
        img.save(buffer, format=self.enc)
        self.img = buffer

    def get_img(self):
        return Image.open(self.img)

    def get_label(self):
        raw = np.frombuffer(self.label, dtype=self.lb_dtype)
        raw.shape = self.lb_shape
        return raw


class DBWriter:
    def __init__(self, db_name_folder):
        self.db_path = db_name_folder
        if os.path.exists(self.db_path):
            print("DB {} already exists. New data will be appended".format(self.db_path))
        os.system("mkdir -p {}".format(self.db_path))
        self.index = 0

    def StartWrite(self):
        self.db = lmdb.open(self.db_path, map_async=True,
                            max_dbs=0, writemap=True)
        self.index = self.db.stat()["entries"]

    def WriteBatch(self, batch):
        for img_lb in batch:
            key = r"{}".format(self.index)
            value = Serialize(img_lb)
            self._write_to_lmdb(key.encode("ascii"), value)
            self.index += 1

    def WriteOne(self, data):
        key = r"{}".format(self.index)
        value = Serialize(data)
        self._write_to_lmdb(key.encode("ascii"), value)
        self.index += 1

    def EndWrite(self):
        self.db.close()

    def _write_to_lmdb(self, key, value):
        success = False
        while not success:
            txn = self.db.begin(write=True)
            try:
                txn.put(key, value)
                txn.commit()
                success = True
            except lmdb.MapFullError:
                txn.abort()

                # increase the map_size
                curr_limit = self.db.info()['map_size']
                new_limit = int(curr_limit * 1.1)
                print("Increasing DB size in 10% !")
                self.db.set_mapsize(new_limit)  # double it


def Serialize(data: ImageLabelPairEncoder):
    return pickle.dumps(data)

def Deserialize(data: bytes):
    return pickle.loads(data)

def create_db(output_folder, input_folder, images, labels, c, w, h):
    color_mode = "L" if c == 1 else "RGB"
    CM = color_mode

    print("No. of images: {}".format(len(images)))
    print("Color mode   : {}".format(CM))
    print("Width        : {}".format(w))
    print("Height       : {}".format(h))
    print("Channels     : {}".format(c))
    img_db = DBWriter(output_folder)
    img_db.StartWrite()
    for i in range(len(images)):

        if isabs(images[i]):
            img_path = images[i]
        else:
            img_path = join(input_folder, images[i])

        p_img = Image.open(img_path)

        if (w != -1 and h != -1) and (p_img.width != w or p_img.height != h):
            p_img = p_img.resize((w, h))
              
        p_img = p_img.convert(mode=color_mode)

        img_db.WriteOne(ImageLabelPairEncoder(p_img, labels[i]))
        print("image: {:6}/{}".format(i, len(images)), end="\r")
    img_db.EndWrite()
    print("Dataset ready: {}".format(output_folder))


def read_lst_file(lst_path, do_shuffle=False):
    print("Shuffle: {}".format(do_shuffle))
    f = open(lst_path)
    names = []
    labels = []
    for line in f:
        s = line.split()
        if len(s) < 2:
            break

        nm = s[0].strip()
        names.append(nm)

        lb = tuple(map(float, s[1:]))
        labels.append(np.array(lb, dtype=np.float32))

    img_dir, _ = split(lst_path)

    image_lst = np.array(names)
    label_lst = labels
    if do_shuffle:
        inds = np.arange(len(image_lst))
        np.random.shuffle(inds)
        image_lst = image_lst[inds]
        label_lst = [labels[i] for i in inds]

    return img_dir, image_lst, label_lst

if __name__ == '__main__':
    pass
