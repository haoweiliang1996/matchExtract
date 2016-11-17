#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Tianming Lu
# adapted by: Nicolas Rangeon
import re
from functools import reduce
'''
content="在/p  １９９８年/t  来临/v  之际/f  ，/w  我/r  十分/m  高兴/a  地/u  通过/p  [中央/n  人民/n  广播/vn  电台/n]nt  、/w  [中国/ns  国际/n  广播/vn  电台/n]nt  和/c  [中央/n  电视台/n]nt  ，/w  向/p  全国/n  各族/r  人民/n  ，/w  向/p  [香港/ns  特别/a  行政区/n]ns  同胞/n  、/w  澳门/ns  和/c  台湾/ns  同胞/n  、/w  海外/s  侨胞/n  ，/w  向/p  世界/n  " \
        "各国/r  的/u  朋友/n  们/k  ，/w  致以/v  诚挚/a  的/u  问候/vn  和/c  良好/a  的/u  祝愿/vn  ！/w  １９９７年/t  ，/w  是/v  中国/ns  发展/vn  历史/n  上/f  非常/d  重要/a  的/u  很/d  不/d  平凡/a  的/u  一/m  年/q  。/w  中国/ns  人民/n  决心/d  继承/v  邓/nr  小平/nr  同志/n  的/u  遗志/n  ，/w  继续/v  把/p  建设/v  有/v  中国/ns  特色/n  社会主义/n  " \
        "事业/n  推向/v  前进/v  。/w  [中国/ns  政府/n]nt  顺利/ad  恢复/v  对/p  香港/ns  行使/v  主权/n  ，/w  并/c  按照/p  “/w  一国两制/j  ”/w  、/w  “/w  港人治港/l  ”/w  、/w  高度/d  自治/v  的/u  方针/n  保持/v  香港/ns  的/u  繁荣/an  稳定/an  。/w  [中国/ns  共产党/n]nt  成功/a  地/u  召开/v  了/u  第十五/m  次/q  全国/n  代表大会/n  ，/w  高举/v  邓小平理论/n  " \
        "伟大/a  旗帜/n  ，/w  总结/v  百年/m  历史/n  ，/w  展望/v  新/a  的/u  世纪/n  ，/w  制定/v  了/u  中国/ns  跨/v  世纪/n  发展/v  的/u  行动/vn  纲领/n  。/w  "
'''
pa="[A-Za-z0-9\`\~\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\{}《》？、.、\“\”——\n’（）()--『』\、、“\”：]"#"[A-Za-z0-9\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]"
with open("inputdate.in","r") as f:
    content=f.read()
str1=re.sub(pa,"",content)
r=re.compile("[，。；！]")
strlist=r.split(str1)
itemsSet=list(map(lambda x:"".join(x).split(" "),strlist))
itemsSet=list(map(lambda x:list(filter(lambda y:len(y),x)),itemsSet))
itemsSet=list(filter(lambda x:len(x),itemsSet))
kount=0
for i in range(len(itemsSet)):
    kount+=len(itemsSet[i])
for i in range(len(itemsSet)):
    itemsSet[i]=list(map (lambda x:x.split(" "),itemsSet[i]))
#print(itemsSet)
rate=0.02
#print(int(kount))


# print(int(rate*kount))


class PrefixSpan:
    def __init__(self, sequences, minSupport=0.1, maxPatternLength=10):

        minSupport = minSupport * len(sequences)
        self.PLACE_HOLDER = '_'

        freqSequences = self._prefixSpan(
            self.SequencePattern([], None, maxPatternLength, self.PLACE_HOLDER),
            sequences, minSupport, maxPatternLength)

        self.freqSeqs = PrefixSpan.FreqSequences(freqSequences)

    @staticmethod
    def train(sequences, minSupport=0.1, maxPatternLength=10):
        return PrefixSpan(sequences, minSupport, maxPatternLength)

    def freqSequences(self):
        return self.freqSeqs

    class FreqSequences:
        def __init__(self, fs):
            self.fs = fs

        def collect(self):
            return self.fs

    class SequencePattern:
        def __init__(self, sequence, support, maxPatternLength, place_holder):
            self.place_holder = place_holder
            self.sequence = []
            for s in sequence:
                self.sequence.append(list(s))
            self.freq = support

        def append(self, p):
            if p.sequence[0][0] == self.place_holder:
                first_e = p.sequence[0]
                first_e.remove(self.place_holder)
                self.sequence[-1].extend(first_e)
                self.sequence.extend(p.sequence[1:])
            else:
                self.sequence.extend(p.sequence)
                if self.freq is None:
                    self.freq = p.freq
            self.freq = min(self.freq, p.freq)

    def _checkPatternLengths(self, pattern, maxPatternLength):
        for s in pattern.sequence:
            if len(s) > maxPatternLength:
                return False
        return True

    def _prefixSpan(self, pattern, S, threshold, maxPatternLength):
        patterns = []

        if self._checkPatternLengths(pattern, maxPatternLength):
            f_list = self._frequent_items(S, pattern, threshold, maxPatternLength)

            for i in f_list:
                p = self.SequencePattern(pattern.sequence, pattern.freq, maxPatternLength, self.PLACE_HOLDER)
                p.append(i)
                if self._checkPatternLengths(pattern, maxPatternLength):
                    patterns.append(p)

                p_S = self._build_projected_database(S, p)
                p_patterns = self._prefixSpan(p, p_S, threshold, maxPatternLength)
                patterns.extend(p_patterns)

        return patterns

    def _frequent_items(self, S, pattern, threshold, maxPatternLength):
        items = {}
        _items = {}
        f_list = []
        if S is None or len(S) == 0:
            return []

        if len(pattern.sequence) != 0:
            last_e = pattern.sequence[-1]
        else:
            last_e = []
        for s in S:

            # class 1
            is_prefix = True
            for item in last_e:
                if item not in s[0]:
                    is_prefix = False
                    break
            if is_prefix and len(last_e) > 0:
                index = s[0].index(last_e[-1])
                if index < len(s[0]) - 1:
                    for item in s[0][index + 1:]:
                        if item in _items:
                            _items[item] += 1
                        else:
                            _items[item] = 1

            # class 2
            if self.PLACE_HOLDER in s[0]:
                for item in s[0][1:]:
                    if item in _items:
                        _items[item] += 1
                    else:
                        _items[item] = 1
                s = s[1:]

            # class 3
            counted = []
            for element in s:
                for item in element:
                    if item not in counted:
                        counted.append(item)
                        if item in items:
                            items[item] += 1
                        else:
                            items[item] = 1

        f_list.extend([self.SequencePattern([[self.PLACE_HOLDER, k]], v, maxPatternLength, self.PLACE_HOLDER)
                       for k, v in _items.items()
                       if v >= threshold])
        f_list.extend([self.SequencePattern([[k]], v, maxPatternLength, self.PLACE_HOLDER)
                       for k, v in items.items()
                       if v >= threshold])

        # todo: can be optimised by including the following line in the 2 previous lines
        f_list = [i for i in f_list if self._checkPatternLengths(i, maxPatternLength)]

        sorted_list = sorted(f_list, key=lambda p: p.freq)
        return sorted_list

    def _build_projected_database(self, S, pattern):
        """
		suppose S is projected database base on pattern's prefix,
		so we only need to use the last element in pattern to
		build projected database
		"""
        p_S = []
        last_e = pattern.sequence[-1]
        last_item = last_e[-1]
        for s in S:
            p_s = []
            for element in s:
                is_prefix = False
                if self.PLACE_HOLDER in element:
                    if last_item in element and len(pattern.sequence[-1]) > 1:
                        is_prefix = True
                else:
                    is_prefix = True
                    for item in last_e:
                        if item not in element:
                            is_prefix = False
                            break

                if is_prefix:
                    e_index = s.index(element)
                    i_index = element.index(last_item)
                    if i_index == len(element) - 1:
                        p_s = s[e_index + 1:]
                    else:
                        p_s = s[e_index:]
                        index = element.index(last_item)
                        e = element[i_index:]
                        e[0] = self.PLACE_HOLDER
                        p_s[0] = e
                    break
            if len(p_s) != 0:
                p_S.append(p_s)

        return p_S


if __name__ == "__main__":

    sequences = itemsSet#[[['在'], ['１９９８年'], ['来临'], ['之际']], [['我'], ['十分'], ['高兴'], ['地'], ['通过'], ['中央'], ['人民'], ['广播'], ['电台'], ['、'], ['中国'], ['国际'], ['广播'], ['电台'], ['和'], ['中央'], ['电视台']], [['向'], ['全国'], ['各族'], ['人民']], [['向'], ['香港'], ['特别'], ['行政区'], ['同胞'], ['、'], ['澳门'], ['和'], ['台湾'], ['同胞'], ['、'], ['海外'], ['侨胞']], [['向'], ['世界'], ['各国'], ['的'], ['朋友'], ['们']], [['致以'], ['诚挚'], ['的'], ['问候'], ['和'], ['良好'], ['的'], ['祝愿'], ['１９９７年']], [['是'], ['中国'], ['发展'], ['历史'], ['上'], ['非常'], ['重要'], ['的'], ['很'], ['不'], ['平凡'], ['的'], ['一'], ['年']], [['中国'], ['人民'], ['决心'], ['继承'], ['邓'], ['小平'], ['同志'], ['的'], ['遗志']], [['继续'], ['把'], ['建设'], ['有'], ['中国'], ['特色'], ['社会主义'], ['事业'], ['推向'], ['前进']], [['中国'], ['政府'], ['顺利'], ['恢复'], ['对'], ['香港'], ['行使'], ['主权']], [['并'], ['按照'], ['“'], ['一国两制'], ['”'], ['、'], ['“'], ['港人治港'], ['”'], ['、'], ['高度'], ['自治'], ['的'], ['方针'], ['保持'], ['香港'], ['的'], ['繁荣'], ['稳定']], [['中国'], ['共产党'], ['成功'], ['地'], ['召开'], ['了'], ['第十五'], ['次'], ['全国'], ['代表大会']], [['高举'], ['邓小平理论'], ['伟大'], ['旗帜']], [['总结'], ['百年'], ['历史']], [['展望'], ['新'], ['的'], ['世纪']], [['制定'], ['了'], ['中国'], ['跨'], ['世纪'], ['发展'], ['的'], ['行动'], ['纲领']]]

    # print(sequences)
    supp=0.0005/3
    model = PrefixSpan.train(sequences, minSupport=(supp), maxPatternLength=5)
    result = model.freqSequences().collect()
   # print('begin')
    for fs in result:
        # print "你好",fs.sequence
        # print fs.sequence
        if len(fs.sequence) > 1:
            #print('{},{}'.format(fs.sequence,fs.freq))
            print('{}'.format("".join(list(reduce(lambda a, b: a + [" "] + b, fs.sequence)))))
