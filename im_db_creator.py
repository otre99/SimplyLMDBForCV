from ImgDB import create_db, read_lst_file
import argparse

########################################################################


def create_parser():
    parser = argparse.ArgumentParser(
        description="Create an LMDB dataset from existing tagged images")
    parser.add_argument('input_file', type=str,
                        help="Input file (line: image_path  label_1 label_2 ... label_n)")
    parser.add_argument('--output_folder', type=str, default="./",
                        help="Output dataset folder")
    parser.add_argument('--channels', type=int, default=3,
                        help="Number of channels of the input images (1-GRAY 3-RBG)")
    parser.add_argument('--width', type=int, default=-1,
                        help="Input image width")
    parser.add_argument('--height', type=int, default=-1,
                        help="Input image height")
    parser.add_argument('--shuffle', type=bool, default=False,
                        help="Shuffle images list before create the dataset")

    return parser


if __name__ == '__main__':
    p = create_parser()
    FLAGS, unparsed_args = p.parse_known_args()
    if len(unparsed_args):
        print("Warning: unknow arguments {}".format(unparsed_args))

    input_folder, images, labels = read_lst_file(
        FLAGS.input_file, do_shuffle=FLAGS.shuffle)
    create_db(output_folder=FLAGS.output_folder,
              input_folder=input_folder,
              images=images,
              labels=labels,
              c=FLAGS.channels,
              h=FLAGS.height,
              w=FLAGS.width)
