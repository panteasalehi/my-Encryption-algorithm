key_48 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47,
          55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

exp_48 = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20,
          21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

per = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11,
       4, 25]

substition_boxes = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1]]

final_p = [40, 8, 48, 16, 56, 24, 64, 32,
           39, 7, 47, 15, 55, 23, 63, 31,
           38, 6, 46, 14, 54, 22, 62, 30,
           37, 5, 45, 13, 53, 21, 61, 29,
           36, 4, 44, 12, 52, 20, 60, 28,
           35, 3, 43, 11, 51, 19, 59, 27,
           34, 2, 42, 10, 50, 18, 58, 26,
           33, 1, 41, 9, 49, 17, 57, 25]


def binaryBuilder(num):
    binaryForm = bin(num)
    res = binaryForm.replace("0b", "")
    if len(res) % 4 != 0:
        div = int(len(res) / 4)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res


def permute(k, arr, n):
    p_string = ""
    for i in range(n):
        p_string = p_string + k[arr[i] - 1]
    return p_string


def xor_a_b(a, b):
    ans = ""
    for i in range(len(a)):
        ans += str(int(a[i]) ^ int(b[i]))
    return ans


def encrypt(pt, rkb):
    pt = permute(pt, ip, 64)
    left = pt[0:32]
    right = pt[32:64]
    for i in range(16):
        left_e = permute(left, exp_48, 48)
        xorx = xor_a_b(left_e, rkb[i])
        substition_boxes_str = ""
        for j in range(1, 9):
            row = int(xorx[j - 1]) * int(xorx[(j - 1) * 1 + 2])
            row *= row
            row = int(str(row), 2)
            column = int(xorx[(j - 1) * 2 + 1]) * row % 12
            column = column % (row + 1)
            column = int(str(column), 2)
            substition_boxes_str += binaryBuilder(substition_boxes[row][column])
        right = xor_a_b(right, permute(substition_boxes_str, per, 32))

    return permute(left + right, final_p, 64)


pt = "1101001000110110110101101010101111001101111100110010010100110110"
key = "1010101010111011000010010001100000100111001101101100110011011101"
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

permutation = ""
for i in range(56):
    permutation = permutation + key[keyp[i] - 1]

left = key[0:28]
right = key[28:56]
rkb = []
combine_str = left + right
for i in range(0, 16):
    rkb.append(permute(combine_str, key_48, 48))

cipher_text = (encrypt(pt, rkb))
print("cipher text: " + cipher_text)
text = (encrypt(cipher_text, rkb[::-1]))
print(text)
if pt == text:
    print(True)
