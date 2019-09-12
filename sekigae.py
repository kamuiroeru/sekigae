from random import shuffle, seed
from math import log10, floor

seed(1)


class Sekigae:
    def _make_table_position(self, n_people, ncol):
        """
        人数から席配置を示した2次元リストを作る
        """
        outer_list = []
        people = list(range(1, n_people + 1))
        shuffle(people)
        for left in range(0, n_people, ncol):
            outer_list.append(people[left:left + ncol])

        return outer_list

    def __init__(self, n_people: int, ncol=6, top_label='黒板'):
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
        self.position = self._make_table_position(n_people, ncol)
        self.max_char_width = floor(log10(n_people)) + 1
        self.line_bar = '-' * ((self.max_char_width + 3) * ncol + 1)
        self.header = ('{: ^' + str(len(self.line_bar)) + '}').format(top_label)
        self.table_format = lambda n: \
            ' ' + ' ' * (self.max_char_width - len(str(n))) + str(n) + ' '
        self.make_line = lambda line: '|' + '|'.join([self.table_format(n) for n in line]) + '|'

    def search(self, n: int) -> (int, int):
        """n 番の位置を探す（脳筋実装）"""
        for lc, line in enumerate(self.position):
            if n in line:
                return lc, line.index(n)

    def swap(self, a: int, b: int):
        """a と b の配置を入れ替える"""
        assert 0 < a < self.n_people + 1, f'a は 0 < a < {self.n_people + 1} の範囲のみ指定できます'
        assert 0 < b < self.n_people + 1, f'b は 0 < b < {self.n_people + 1} の範囲のみ指定できます'
        pa = self.search(a)
        pb = self.search(b)
        self.position[pa[0]][pa[1]] = b
        self.position[pb[0]][pb[1]] = a

    def show(self, side='left'):
        """
        席を表示する
        :param str side: "left" or "right" 後ろの席を左寄せにするか右寄せにするか
        :return:
        """
        assert side == 'left' or side == 'right', 'side は "left" か "right" のどちらかです'
        print(self.header)
        print(self.line_bar)
        for line in self.position[:-1]:
            print(self.make_line(line))
            print(self.line_bar)

        # 最後の列
        last = self.make_line(self.position[-1])
        if side == 'right':
            space = ' ' * (len(self.line_bar) - len(last))
            print(space + last)
        else:
            print(last)


if __name__ == '__main__':
    sekigae = Sekigae(45)
    sekigae.show()
