from Klasik_Kripto.sbox_generator import SBoxGenerator

SBOX, INV_SBOX = SBoxGenerator.generate()

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


def _xtime(a):
    return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else (a << 1) & 0xff


def _multiply(a, b):
    result = 0
    for i in range(8):
        if b & 1:
            result ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xff
        if hi_bit:
            a ^= 0x1b
        b >>= 1
    return result


def _sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = SBOX[state[i][j]]


def _inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = INV_SBOX[state[i][j]]


def _shift_rows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]


def _inv_shift_rows(state):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]


def _mix_columns(state):
    for j in range(4):
        a = [state[i][j] for i in range(4)]
        state[0][j] = _multiply(a[0], 2) ^ _multiply(a[1], 3) ^ a[2] ^ a[3]
        state[1][j] = a[0] ^ _multiply(a[1], 2) ^ _multiply(a[2], 3) ^ a[3]
        state[2][j] = a[0] ^ a[1] ^ _multiply(a[2], 2) ^ _multiply(a[3], 3)
        state[3][j] = _multiply(a[0], 3) ^ a[1] ^ a[2] ^ _multiply(a[3], 2)


def _inv_mix_columns(state):
    for j in range(4):
        a = [state[i][j] for i in range(4)]
        state[0][j] = _multiply(a[0], 14) ^ _multiply(a[1], 11) ^ _multiply(a[2], 13) ^ _multiply(a[3], 9)
        state[1][j] = _multiply(a[0], 9) ^ _multiply(a[1], 14) ^ _multiply(a[2], 11) ^ _multiply(a[3], 13)
        state[2][j] = _multiply(a[0], 13) ^ _multiply(a[1], 9) ^ _multiply(a[2], 14) ^ _multiply(a[3], 11)
        state[3][j] = _multiply(a[0], 11) ^ _multiply(a[1], 13) ^ _multiply(a[2], 9) ^ _multiply(a[3], 14)


def _add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]


def _key_expansion(key):
    key_bytes = [b for b in key]
    while len(key_bytes) < 16:
        key_bytes.append(0)
    key_bytes = key_bytes[:16]
    
    w = [[key_bytes[4*j + i] for j in range(4)] for i in range(4)]
    
    round_keys = [[[w[i][j] for j in range(4)] for i in range(4)]]
    
    for round_num in range(10):
        prev = [row[-1] for row in w]
        temp = prev[1:] + prev[:1]
        temp = [SBOX[b] for b in temp]
        temp[0] ^= RCON[round_num]
        
        new_w = []
        for i in range(4):
            new_col = []
            for j in range(4):
                if i == 0:
                    new_col.append(w[j][0] ^ temp[j])
                else:
                    new_col.append(new_w[i-1][j] ^ w[j][i])
            new_w.append(new_col)
        
        w = [[new_w[j][i] for j in range(4)] for i in range(4)]
        round_keys.append([[w[i][j] for j in range(4)] for i in range(4)])
    
    return round_keys


def _bytes_to_state(block):
    return [[block[i + 4*j] for j in range(4)] for i in range(4)]


def _state_to_bytes(state):
    return bytes([state[i][j] for j in range(4) for i in range(4)])


def _pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)


def _unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]


def aes_sifrele(metin, anahtar):
    if isinstance(metin, str):
        metin = metin.encode('utf-8')
    if isinstance(anahtar, str):
        anahtar = anahtar.encode('utf-8')
    
    padded = _pad(metin)
    round_keys = _key_expansion(anahtar)
    
    sifreli = b''
    for i in range(0, len(padded), 16):
        block = padded[i:i+16]
        state = _bytes_to_state(block)
        
        _add_round_key(state, round_keys[0])
        
        for r in range(1, 10):
            _sub_bytes(state)
            _shift_rows(state)
            _mix_columns(state)
            _add_round_key(state, round_keys[r])
        
        _sub_bytes(state)
        _shift_rows(state)
        _add_round_key(state, round_keys[10])
        
        sifreli += _state_to_bytes(state)
    
    return sifreli.hex()


def aes_desifre(sifreli_hex, anahtar):
    if isinstance(anahtar, str):
        anahtar = anahtar.encode('utf-8')
    
    sifreli = bytes.fromhex(sifreli_hex)
    round_keys = _key_expansion(anahtar)
    
    cozulmus = b''
    for i in range(0, len(sifreli), 16):
        block = sifreli[i:i+16]
        state = _bytes_to_state(block)
        
        _add_round_key(state, round_keys[10])
        
        for r in range(9, 0, -1):
            _inv_shift_rows(state)
            _inv_sub_bytes(state)
            _add_round_key(state, round_keys[r])
            _inv_mix_columns(state)
        
        _inv_shift_rows(state)
        _inv_sub_bytes(state)
        _add_round_key(state, round_keys[0])
        
        cozulmus += _state_to_bytes(state)
    
    try:
        return _unpad(cozulmus).decode('utf-8')
    except UnicodeDecodeError:
        return _unpad(cozulmus)
