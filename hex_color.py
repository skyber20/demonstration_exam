# 1 way by format
# def hex_color(r, g, b):
#     return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# colors = (210, 255, 100)
# print(hex_color(*colors))


# 2 way
def perevod(num):
    alph = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    res = ''
    while num > 0:
        remaindner = num % 16
        res += str(remaindner) if remaindner < 10 else alph[remaindner]
        num //= 16
    return res[::-1]

print(perevod(120))
