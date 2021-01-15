from typing import List, Tuple, Iterable

from random import shuffle
from math import log10, floor
import csv
from enum import Enum, auto

Position = List[List[int]]


class Sekigae:
    class Side(Enum):
        left = auto()
        right = auto(

        )
    def _make_table_position(self) -> Position:
        """
        人数から席配置を示した2次元リストを作る
        """
        outer_list: Position = []
        people = list(range(1, self.n_people + 1))
        shuffle(people)
        for left in range(0, self.n_people, self.ncol):
            outer_list.append(people[left:left + self.ncol])

        return outer_list

    def _reload_params(self, position: Position, top_label: str) -> None:
        self.n_people = sum(len(e) for e in position)
        self.ncol = len(position[0])
        self.max_char_width = floor(log10(self.n_people)) + 1
        self.line_bar = '-' * ((self.max_char_width + 3) * self.ncol + 1)
        self.header = ('{: ^' + str(len(self.line_bar)) + '}').format(top_label)
        self.table_format = lambda n: \
            ' ' + ' ' * (self.max_char_width - len(str(n))) + str(n) + ' '
        self.make_line = lambda line: '|' + '|'.join([self.table_format(n) for n in line]) + '|'

    def __init__(self, n_people: int, ncol: int = 6, top_label: str = '黒板') -> None:
        """
        人数から席配置を示した2次元リストを作る
        :param int n_people: 席につく人数
        :param int ncol: 何列に配置するか（Default: 6）
        :param str top_label: '前' の表示名（Default: "黒板"）
        """
        assert n_people > 0, '人数は 1 以上を指定してください'
        assert ncol > 0, '列数は 1 以上を指定してください'
        assert n_people > ncol, '人数 > 列数 となるように指定してください'

        self.n_people = n_people
        self.ncol = ncol
        self.position = self._make_table_position()
        self.max_char_width = floor(log10(n_people)) + 1
        self.line_bar = '-' * ((self.max_char_width + 3) * ncol + 1)
        self.header = ('{: ^' + str(len(self.line_bar)) + '}').format(top_label)
        self.table_format = lambda n: \
            ' ' + ' ' * (self.max_char_width - len(str(n))) + str(n) + ' '
        self.make_line = lambda line: '|' + '|'.join([self.table_format(n) for n in line]) + '|'

    def search(self, n: int) -> Tuple[int, int]:
        """n 番の位置を探す（脳筋実装）"""
        for lc, line in enumerate(self.position):
            if n in line:
                return lc, line.index(n)

    def swap(self, a: int, b: int) -> None:
        """a と b の配置を入れ替える"""
        assert 0 < a < self.n_people + 1, f'a は 0 < a < {self.n_people + 1} の範囲のみ指定できます'
        assert 0 < b < self.n_people + 1, f'b は 0 < b < {self.n_people + 1} の範囲のみ指定できます'
        pa = self.search(a)
        pb = self.search(b)
        self.position[pa[0]][pa[1]] = b
        self.position[pb[0]][pb[1]] = a

    def set(self, x: int, y: int, n: int) -> None:
        """
        n を x 行 y 列 にセットする。もともとそこにあった番号が n と入れ替わる
        :param x: 行数
        :param y: 列数
        :param n: セットする番号
        """
        a = n
        try:
            b = self.position[x-1][y-1]
        except IndexError:
            assert False, 'そこに席はありません'
        self.swap(a, b)

    def show(self, side: Side = Side.left) -> None:
        """
        席を表示する
        :param str side: "left" or "right" 後ろの席を左寄せにするか右寄せにするか
        :return:
        """
        assert isinstance(side, self.Side), 'side は Side.left か Side.right のどちらかです'
        print(self.header)
        print(self.line_bar)
        for line in self.position[:-1]:
            print(self.make_line(line))
            print(self.line_bar)

        # 最後の列
        last = self.make_line(self.position[-1])
        if side == self.Side.right:
            space = ' ' * (len(self.line_bar) - len(last))
            print(space + last)
        else:
            print(last)

    def to_csv(self, filename: str = 'out.csv') -> None:
        """
        席の並びをcsvに吐き出す
        :param str filename: 書き出すCSVファイル名（default: "out.csv"）
        """
        with open(filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.position)

    def read_csv_iter(self, iterable: Iterable, top_label: str) -> None:
        """
        iterable な Object から CSV を読み込む
        :param iter iterable: iterable
        :param str top_label: label
        :return:
        """
        reader = csv.reader(iterable)
        self.position = [[int(elem) for elem in inner] for inner in reader]
        self._reload_params(self.position, top_label)

    def read_csv(self, filename: str, top_label: str = '黒板') -> None:
        """
        席の並びが書いてあるcsvを読み込む
        :param str filename: 読み込むCSVファイル名
        :param str top_label: '前' の表示名（Default: "黒板"）
        """
        with open(filename) as f:
            self.read_csv_iter(f, top_label)

    def show_csv(self) -> None:
        """CSV形式で出力する（UNIXパイプライン処理用）"""
        s = '\n'.join([','.join(map(str, inner)) for inner in self.position])
        print(s)
