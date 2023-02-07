from ImgDB import DBReader, ImageLabelPairEncoder
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="Create an LMDB dataset from existing tagged images")
    parser.add_argument('db', type=str, help="Input Dataset")
    return parser

if __name__ == "__main__":
    import matplotlib.pyplot as plt 

    p = create_parser()
    FLAGS, unparsed_args = p.parse_known_args()
    if len(unparsed_args):
        print("Warning: unknow arguments {}".format(unparsed_args))

    db = DBReader(FLAGS.db)
    n = len(db)
    while True:
        ii = input("Integer number [0, {}] for display or -1 for exit: ".format(n))
        ii = int(ii)
        if ii==-1: break
        if not (0<=ii<n):
            print("Index out of range")
            continue 
        image, labels = db[ii]
        plt.title(labels)
        plt.imshow(image)
        plt.show()
