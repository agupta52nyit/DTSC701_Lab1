def dia_prob(msg):
    compressed_msg = ""
    count = 1

    for i in range(1, len(msg)):
        if msg[i] == msg[i-1]:
            count += 1
        else:
            if count > 1:
                compressed_msg += f"{msg[i-1]}{count}"
            else:
                compressed_msg += msg[i-1]
            count = 1

    #Last character
    if count > 1:
        compressed_msg += f"{msg[-1]}{count}"
    else:
        compressed_msg += msg[-1]

    print(compressed_msg)

if __name__ == '__main__':
    input_1 = "abcaaabbb"
    input_2 = "abcd"

    dia_prob(input_1)
    dia_prob(input_2)