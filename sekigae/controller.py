import argparse
from sekigae import Sekigae
from sys import stdin


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


def main():
    parser = argparse.ArgumentParser(formatter_class=CustomFormatter, description='Sekigae Program')
    parser.add_argument('-t', '--tag', default='FRONT',
                        help='set tag name\n')
    parser.add_argument('-o', '--out',
                        help='Write Tables to CSV File\n')
    parser.add_argument('-f', '--format', action='store_true',
                        help='Output Tables as CSV Style\n')
    _format = lambda s: [tuple(map(int, order.split(':'))) for order in s.split(',')]
    parser.add_argument('-s', '--special', type=_format,
                        help='select number to especially place. \nFormat: row:col:number,...\n')
    if stdin.isatty():
        # UNIXパイプラインinput無し
        parser.add_argument('n_people', type=int,
                            help='Number of people')
        parser.add_argument('ncol', type=int,
                            help='Number of columns')
        parser.add_argument('--csv',
                            help='Read CSV File (ignore n-people and nrow options)\n')
        args = parser.parse_args()

        seki = Sekigae(args.n_people, args.ncol, args.tag)

        # Read CSV
        if args.csv:
            seki.read_csv(args.csv, args.tag)
    else:
        # UNIXパイプラインinputあり
        args = parser.parse_args()

        seki = Sekigae(2, 1, args.tag)

        # apply stdin CSV
        if not stdin.isatty():
            seki.read_csv_iter(stdin, args.tag)

    # apply special order
    if args.special:
        for order in args.special:
            seki.set(*order)

    # show tables
    if args.format:
        seki.show_csv()
    else:
        seki.show()

    # Write CSV
    if args.out:
        seki.to_csv(args.out)
        if not args.format:
            print('csv wrote')


if __name__ == '__main__':
    main()
