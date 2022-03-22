def makePattern(p):
    tmp = {}    # 문자에 부여한 번호를 임시로 저장하기 위한 사전 리스트
    res = []    # 패턴 결과를 담을 리스트
    index = 0   # 문자에 부여할 번호
    for c in p:
        if c in tmp:
            res.append(tmp[c])
        else:
            tmp[c] = str(index)
            res.append(str(index))
            index += 1
    return ';'.join(res)

def findPattern(msg, p):
    pattern = makePattern(p)
    blocksize = len(p)
    pos = 0
    while True:
        data = msg[pos:pos + blocksize]
        if len(data) < blocksize:
            break
        ptrn = makePattern(data)
        if ptrn == pattern:
            return data
            break
        pos += 1

if __name__ == "__main__":
    msg = '53%%#305))6*;4826)4%=\')4%);806*;48#8@60\'))85;1%(;:-%*8#83(88)5*#;46(;88*96*?;8)*%(;485); \
    5*#2:*%(;4956*2(5*c4)8@8*;4069285);)6#8)4%%;1(%9;48081;8:8%1;48#85;4\')-485#528806*81(%9;48;(88;4(%?34;48)4%; \
    161;:188;%?;'     # cipher text
    known_plaintext = ['goodglass', 'mainbranch']
    for p in known_plaintext:
        ret = findPattern(msg, p)
        print('[{}] = [{}]'.format(p, ret))