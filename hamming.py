from random import randint, random
import math

class Characters:
    def __init__(self, char, freq) -> None:
        self._char = char
        self._freq = freq
        self._code = ""

    def __lt__(self, other):  # method for sorting
        return True if self._freq < other.get_freq() else False

    def __str__(self):
        return "{0}\t {1}\t {2}".format(self._char, str(self._freq), self._code)

    def __iter__(self):
        return self

    def get_char(self):
        return self._char

    def get_freq(self):
        return self._freq

    def get_code(self):
        return self._code

    def append_code(self, code):
        self._code += str(code)


# Dividing to left and right, merging Shannon pathways
def DivideList(lst):
    if len(lst) == 1:
        return None
    s = k = b = 0
    for p in lst:
        s += p.get_freq()  # Counting frequency for each character
    s /= 2
    for p in range(len(lst)):
        k += lst[p].get_freq()  # s half of all counted freq, compare it with other parts
        if k == s:
            return p
        elif k > s:
            j = len(lst) - 1
            while b < s:
                b += lst[j].get_freq()
                j -= 1
            return p if abs(s - k) < abs(s - b) else j
    return


# Assigning 0 and 1 to divided groups
def Shannon_fano_code(lst):
    middle = DivideList(lst)
    if middle is None:
        return
    for i in lst[: middle + 1]:  # assign freq for left, by sides until divided middle
        i.append_code(0)
    Shannon_fano_code(lst[: middle + 1])
    for i in lst[middle + 1:]:
        i.append_code(1)
    Shannon_fano_code(lst[middle + 1:])


# Decoding encoded bits to file
def ShannonDecode(dictionary, text):
    res = ""
    while text:
        for k in dictionary:
            if text.startswith(k):
                res += dictionary[k]
                text = text[len(k):]
    return res


# sorting probability in descending order
def sorted_probability(sorting_list):
    desc = sorted(sorting_list, key=lambda x: x[1], reverse=True)
    return desc


# Adding all char with probability to new list by addressing from var Character
def get_all(probabilities):
    lst = []
    for key, value in probabilities:
        lst.append(Characters(key, value))
    return lst

def check(r):
    r1=" "
    r2=" "
    r1=list(r)
    l=len(r)

    if l % 4 ==1:
        r1.append([0,0,0])
    if l % 4 ==2:
        r1.append([0,0])
    if l % 4 ==3:
        r1.append('0')
    
    r2= ''.join(r1) 
    return r2


def my_xor(bits):
    if bits.count('1') % 2 == 1:
        return '1'
    else:
        return '0'

def HammingEncode(r):
        
        lst = []
        encode = []
        result_h = ''
        result = ''
        for i in r:
            encode.append(i)
            if len(encode) == 4:
                a = ''.join(encode)
                lst.append(a)
                encode = []
        # print(lst)

        for i in lst:
            r1 = int(i[0]) ^ int(i[1]) ^ int(i[2])
            r2 = int(i[1]) ^ int(i[2]) ^ int(i[3])
            r3 = int(i[0]) ^ int(i[1]) ^ int(i[3])

            i += str(r1) + str(r2) + str(r3)
            result += i + ' '
            result_h += i

            hammingFile = open("haming.txt", "w+")
            hammingFile.write(result_h)
            hammingFile.close()
        # print(result)

def Divide_7(encoded):
    lst2 = []
    encode = []
    for i in encoded:
        encode.append(i)
        if len(encode) == 7:
            a = ''.join(encode)
            lst2.append(a)
            encode = []
    return list(lst2)
        


if __name__ == "__main__":
    f = open('hah.txt', 'r')
    test_str = f.read()
    total = len(test_str)

    all_freq = {}
    lists = []
    r = ""  # encoded

    # decoded
    code = []
    char = []

    for i in test_str:
        all_freq[i] = test_str.count(i)
    for key, value in all_freq.items():
        prob = round(value / total, 4)
        lists.append((key, prob))
    # print("Probabilities of each char: \n", lists)

    result = sorted_probability(lists)
    # print("Sorted probabilities: \n", result)

    all = get_all(result)

    all.sort(reverse=True)
    encoded_data = []
    Shannon_fano_code(all)
    for c in all:
        encoded_data.append(c)
        # print(c)
    # Getting encoded format of txt
    for u in test_str:
        for n in all:
            if u == n.get_char():
                r += str(n.get_code())

    # Create dictionary by adding code and characters
    for k in all:
        code.append(k.get_code())
        char.append(k.get_char())
    # print(code)
    # print(char)

    # print("Encoded message: \n", r)
    # call decoding method and write decoded test to txt file
    dictionary = dict(zip(code, char))
    decodedFile = open("turned.txt", "w+")
    decodedFile.write(ShannonDecode(dictionary, r))
    decodedFile.close()

    r=check(r)
    
    # print(r)
    HammingEncode(r)
    
    fil = open('haming.txt', 'r')
    tst = fil.read()
    test2 = Divide_7(tst)
    print('Divided into 7 bits list: \n', test2)
    print(test2[0])
        
        
    # test = ['1111110', '1111111', '1111111', '0000000', '0101011']
    test = Divide_7(tst)

    blocksize = len(test)
    blocklength = len(test[0])


    def ErrGen(blocksize):
        percent = randint(10, 50)
        error_count = math.ceil((percent/100) * blocksize)
        return error_count
    
    error_count = ErrGen(blocksize)
    errored_list = []
    for i in range(0, error_count):
        errored_num = 0
        while True:
            errored_num = randint(0, blocksize - 1)
            c = [i for i in errored_list if i == errored_num]
            if len(c) == 0:
                break
            else:
                continue
        errored_list.append(errored_num)
        random_pos = randint(0, len(test[errored_num]) - 1)
        if test[errored_num][random_pos] == '0':
            test[errored_num] = test[errored_num][:random_pos] + '1' + test[errored_num][random_pos + 1:]

        else:
            test[errored_num] = test[errored_num][:random_pos] + '0' + test[errored_num][random_pos + 1:]

    errored_list.sort()
    fileChic = open('Errored.txt', 'w+')
    print('Errors: \n')
    for i in errored_list:
        print(str(i) + ': ' + test[i])
        fileChic.write(test[i])
    errors = ''.join(test)
    print(errors)
