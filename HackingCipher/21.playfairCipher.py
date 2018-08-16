# Frequency Finder
# http://inventwithpython.com/hacking (BSD Licensed)
import sys

'''
    本程序中的密码表是按照列填充的，还可以按照行填充
    本程序选择去掉J，其实应该去掉一个出现频率最低的字母
    对于密码表中没有出现字母，应该如何加密？
'''
# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
                     'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
                     'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# 明文
message = 'ItisnotaproblemItisachallengeEnjoyfacingit'
# 密钥
key = 'boysandgirlsarestudents'
# 不能够使用的字母 长度=len(LETTERS)-25
notUseLetter = ['J']
# 如果成对后有两个相同字母紧挨或最后一个字母是单个的，就插入一个字母X（或者Q）
insertLetter = 'Q'
# 是要加密还是要解密
mode = 'encrypt'
#mode = 'decrypt'


# 得到密码表 按照行填充
# 密码表1 方便使用坐标定位
# 密码表2 方便使用字母定位
def getMiMaBiao(key):
    res = ''
    for k in key.upper():
        if (not k in LETTERS) or (k in res):
            continue
        res = res + k
    for LETTER in LETTERS:
        if LETTER in res:
            continue
        res = res + LETTER
    for LETTER in notUseLetter:
        res = res.replace(LETTER, '')

    miMaBiao1 = [['x'] * 5, ['x'] * 5, ['x'] * 5, ['x'] * 5, ['x'] * 5]
    miMaBiao2 = {}
    i = 0
    for row in range(0, 5):
        for col in range(0, 5):
            miMaBiao1[row][col] = res[i]
            miMaBiao2[res[i]] = (row, col)
            i = i + 1

    return miMaBiao1, miMaBiao2


# 对一个字母单元进行加密
def encryptUnit(miMaBiaos, unit):
    if len(unit) != 2:
        print("playfair体制要求加密的单元的长度为2")
        sys.exit()
    if unit[0] == unit[1]:
        print("playfait体制要求加密的单元的两个字母互不相同")
        sys.exit()
    row1, col1 = miMaBiaos[1][unit[0]]
    row2, col2 = miMaBiaos[1][unit[1]]

    # 横向替换
    if row1 != row2 and col1 != col2:
        return miMaBiaos[0][row1][col2] + miMaBiaos[0][row2][col1]
    # 取右边的字母
    elif row1 == row2:
        return miMaBiaos[0][row1][(col1 + 1) % 5] + miMaBiaos[0][row1][(col2 + 1) % 5]
    # 取下边的字母
    elif col1 == col2:
        return miMaBiaos[0][(row1 + 1) % 5][col1] + miMaBiaos[0][(row2 + 1) % 5][col2]


# 对一个字母单元进行加密
def decryptUnit(miMaBiaos, unit):
    if len(unit) != 2:
        print("playfair体制要求加密的单元的长度为2")
        sys.exit()
    if unit[0] == unit[1]:
        print("playfait体制要求加密的单元的两个字母互不相同")
        sys.exit()
    row1, col1 = miMaBiaos[1][unit[0]]
    row2, col2 = miMaBiaos[1][unit[1]]

    # 横向替换
    if row1 != row2 and col1 != col2:
        return miMaBiaos[0][row1][col2] + miMaBiaos[0][row2][col1]
    # 取右边的字母
    elif row1 == row2:
        return miMaBiaos[0][row1][(col1 - 1 + 5) % 5] + miMaBiaos[0][row1][(col2 - 1 + 5) % 5]
    # 取下边的字母
    elif col1 == col2:
        return miMaBiaos[0][(row1 - 1 + 5) % 5][col1] + miMaBiaos[0][(row2 - 1 + 5) % 5][col2]


# 将明文每两个字母组成一对。如果成对后有两个相同字母紧挨或最后一个字母是单个的，就插入一个字母X（或者Q）。
# 1.将明文全部大写
# 2.将明文拆分为若干unit
def getUnits(message):
    res = ''
    for m in message.upper():
        if m == res[-1::1] and len(res) % 2 == 1:
            res = res + insertLetter + m
        else:
            res = res + m

    if len(res) % 2 == 1:
        res = res + insertLetter

    return [res[i:i + 2] for i in range(0, len(res), 2)]


def translate(miMaBiaos, message, mode):
    units = getUnits(message)
    res = ''
    for unit in units:
        if mode == 'encrypt':
            res = res + encryptUnit(miMaBiaos, unit)
        else:
            res = res + decryptUnit(miMaBiaos, unit)
    return res


def main():
    miMaBiao1, miMaBiao2 = getMiMaBiao(key)
    miMaBiaos = (miMaBiao1, miMaBiao2)
    print(translate(miMaBiaos, message.replace('j','i').replace('J','I'), mode))


if __name__ == "__main__":
    main()
