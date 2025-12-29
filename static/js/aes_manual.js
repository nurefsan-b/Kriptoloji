const GaloisField = {
    IRREDUCIBLE_POLY: 0x11b,

    multiply(a, b) {
        let result = 0;
        for (let i = 0; i < 8; i++) {
            if ((b & 1) !== 0) result ^= a;
            const hi_bit_set = (a & 0x80) !== 0;
            a = (a << 1) & 0xFF;
            if (hi_bit_set) a ^= this.IRREDUCIBLE_POLY;
            b >>= 1;
        }
        return result & 0xFF;
    },

    power(a, n) {
        let res = 1;
        while (n > 0) {
            if (n % 2 === 1) res = this.multiply(res, a);
            a = this.multiply(a, a);
            n = Math.floor(n / 2);
        }
        return res;
    },

    inverse(a) {
        if (a === 0) return 0;
        return this.power(a, 254);
    }
};

const SBOX_GEN = (function () {
    const sbox = new Uint8Array(256);
    const inv_sbox = new Uint8Array(256);

    const _rotl8 = (x, shift) => {
        return ((x << shift) | (x >> (8 - shift))) & 0xFF;
    };

    const c = 0x63;

    for (let i = 0; i < 256; i++) {
        let s = GaloisField.inverse(i);
        let s_affine = s ^
            _rotl8(s, 1) ^
            _rotl8(s, 2) ^
            _rotl8(s, 3) ^
            _rotl8(s, 4) ^
            c;

        sbox[i] = s_affine;
        inv_sbox[s_affine] = i;
    }

    return { sbox, inv_sbox };
})();

const SBOX = SBOX_GEN.sbox;
const RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36];

class ManualAES {

    static multiply(a, b) {
        let result = 0;
        for (let i = 0; i < 8; i++) {
            if ((b & 1) !== 0) result ^= a;
            const hi_bit = a & 0x80;
            a = (a << 1) & 0xff;
            if (hi_bit !== 0) a ^= 0x1b;
            b >>= 1;
        }
        return result;
    }

    static subBytes(state) {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                state[i][j] = SBOX[state[i][j]];
            }
        }
    }

    static shiftRows(state) {
        let temp = [...state[1]];
        state[1][0] = temp[1]; state[1][1] = temp[2]; state[1][2] = temp[3]; state[1][3] = temp[0];

        temp = [...state[2]];
        state[2][0] = temp[2]; state[2][1] = temp[3]; state[2][2] = temp[0]; state[2][3] = temp[1];

        temp = [...state[3]];
        state[3][0] = temp[3]; state[3][1] = temp[0]; state[3][2] = temp[1]; state[3][3] = temp[2];
    }

    static mixColumns(state) {
        for (let j = 0; j < 4; j++) {
            const a = [state[0][j], state[1][j], state[2][j], state[3][j]];
            state[0][j] = this.multiply(a[0], 2) ^ this.multiply(a[1], 3) ^ a[2] ^ a[3];
            state[1][j] = a[0] ^ this.multiply(a[1], 2) ^ this.multiply(a[2], 3) ^ a[3];
            state[2][j] = a[0] ^ a[1] ^ this.multiply(a[2], 2) ^ this.multiply(a[3], 3);
            state[3][j] = this.multiply(a[0], 3) ^ a[1] ^ a[2] ^ this.multiply(a[3], 2);
        }
    }

    static addRoundKey(state, roundKey) {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                state[i][j] ^= roundKey[i][j];
            }
        }
    }

    static keyExpansion(key) {
        let keyBytes = [];
        for (let i = 0; i < key.length && i < 16; i++) {
            keyBytes.push(key.charCodeAt(i));
        }
        while (keyBytes.length < 16) keyBytes.push(0);

        let localW = [[], [], [], []];
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                localW[i][j] = keyBytes[4 * j + i];
            }
        }

        let roundKeys = [];
        roundKeys.push(JSON.parse(JSON.stringify(localW)));

        for (let round = 0; round < 10; round++) {
            let prev = [localW[0][3], localW[1][3], localW[2][3], localW[3][3]];
            let temp = [prev[1], prev[2], prev[3], prev[0]];
            temp = temp.map(b => SBOX[b]);
            temp[0] ^= RCON[round];

            let nextW = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
            for (let r = 0; r < 4; r++) {
                nextW[r][0] = localW[r][0] ^ temp[r];
            }
            for (let c = 1; c < 4; c++) {
                for (let r = 0; r < 4; r++) {
                    nextW[r][c] = localW[r][c] ^ nextW[r][c - 1];
                }
            }
            localW = nextW;
            roundKeys.push(JSON.parse(JSON.stringify(localW)));
        }

        return roundKeys;
    }

    static encrypt(text, key) {
        let data = new TextEncoder().encode(text);
        let padLen = 16 - (data.length % 16);
        let padded = new Uint8Array(data.length + padLen);
        padded.set(data);
        for (let i = 0; i < padLen; i++) padded[data.length + i] = padLen;

        let roundKeys = this.keyExpansion(key);
        let encrypted = [];

        for (let i = 0; i < padded.length; i += 16) {
            let block = padded.slice(i, i + 16);
            let state = [[], [], [], []];
            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 4; c++) {
                    state[r][c] = block[r + 4 * c];
                }
            }

            this.addRoundKey(state, roundKeys[0]);

            for (let r = 1; r < 10; r++) {
                this.subBytes(state);
                this.shiftRows(state);
                this.mixColumns(state);
                this.addRoundKey(state, roundKeys[r]);
            }

            this.subBytes(state);
            this.shiftRows(state);
            this.addRoundKey(state, roundKeys[10]);

            for (let c = 0; c < 4; c++) {
                for (let r = 0; r < 4; r++) {
                    encrypted.push(state[r][c]);
                }
            }
        }

        return Array.from(encrypted).map(b => b.toString(16).padStart(2, '0')).join('');
    }
}
