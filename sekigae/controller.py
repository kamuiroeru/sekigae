import argparse
from .sekigae import Sekigae


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


def main():
    parser = argparse.ArgumentParser(formatter_class=CustomFormatter, description='Sekigae Program')
    parser.add_argument('n_people', type=int,
                        help='Number of people')
    parser.add_argument('ncol', type=int,
                        help='Number of columns')
    parser.add_argument('-t', '--tag', default='FRONT',
                        help='set tag name\n')
    parser.add_argument('--csv',
                        help='Read CSV File (ignore n-people and nrow options)\n')
    parser.add_argument('-o', '--out',
                        help='Write Tables to CSV File\n')
    _format = lambda s: [tuple(map(int, order.split(':'))) for order in s.split(',')]
    parser.add_argument('-s', '--special', type=_format,
                        help='select number to especially place. \nFormat: row:col:number,...\n')
    args = parser.parse_args()

    seki = Sekigae(args.n_people, args.ncol, args.tag)

    # Read CSV
    if args.csv:
        seki.read_csv(args.csv, args.tag)

    # apply special order
    if args.special:
        for order in args.special:
            seki.set(*order)

    # show tables
    seki.show()

    # Write CSV
    if args.out:
        seki.to_csv(args.out)
        print('csv wrote')


if __name__ == '__main__':
    main()
