#!/usr/bin/env python3
# Copyright (c) 2020 oatsu
"""
超歌詞すっぴんプラグイン
"""
import jaconv
import utaupy


def force_lyric_zenkaku_hiragana(plugin):
    """
    歌詞に含まれるカタカナとひらがなを、全角ひらがなにする。
    破壊的処理
    """
    for note in plugin.notes:
        lyric = note.lyric
        # 半角カタカナを全角カタカナにする
        lyric = jaconv.h2z(lyric, kana=True, ascii=False, digit=False)
        # カタカナをひらがなにする
        lyric = jaconv.kata2hira(lyric)
        # 無声化とかにつかう歌詞を適当に変更
        lyric = lyric.replace(' s', ' す').replace(' t', ' っ').replace(' k', ' っ')
        # 歌詞を上書きする
        note.lyric = lyric


def suppin_lyric(plugin):
    """
    平仮名以外の文字を歌詞から削除する。
    """
    hiragana_list = [chr(i) for i in range(12353, 12436)]
    for note in plugin.notes:
        original_lyric = note.lyric
        # 休符のとき
        if original_lyric == 'R' or ' R' in original_lyric:
            new_lyric = 'R'
        # 休符でないときは平仮名以外の文字をすべて削除
        else:
            new_lyric = ''.join(
                [character for character in original_lyric if character in hiragana_list])
        # すっぴん化で歌詞が消滅した場合は元の歌詞を使う
        if len(new_lyric) == 0:
            note.lyric = original_lyric
        else:
            note.lyric = new_lyric


def main(plugin):
    """
    平仮名にしてからすっぴん化する。
    """
    force_lyric_zenkaku_hiragana(plugin)
    suppin_lyric(plugin)


if __name__ == '__main__':
    print('Copyright (c) 2021 oatsu')
    print('Copyright (c) 2014 Yukino Ikegami')
    print('Copyright (c) 2001-2020 Python Software Foundation\n')
    utaupy.utauplugin.run(main)
