class ManualRSA {
    static modPow(base, exp, mod) {
        let res = 1n;
        base = base % mod;
        while (exp > 0n) {
            if (exp % 2n === 1n) {
                res = (res * base) % mod;
            }
            base = (base * base) % mod;
            exp = exp / 2n;
        }
        return res;
    }

    static encrypt(text, publicKeyString) {
        const parts = publicKeyString.split(',');
        if (parts.length !== 2) throw new Error("Invalid RSA Key format");

        const e = BigInt(parts[0].trim());
        const n = BigInt(parts[1].trim());

        let encrypted = [];
        for (let i = 0; i < text.length; i++) {
            const charCode = BigInt(text.charCodeAt(i));
            const c = this.modPow(charCode, e, n);
            encrypted.push(c.toString());
        }

        return encrypted.join(',');
    }
}
