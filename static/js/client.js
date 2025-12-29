let ws;
let serverRSAPublicKey;
let localKeyPair;
let sharedSecret;

function connectWebSocket() {
    const urlInput = document.getElementById('server-url').value;
    const statusDiv = document.getElementById('connection-status');

    if (ws) {
        ws.close();
    }

    try {
        ws = new WebSocket(`ws://${urlInput}/ws`);

        ws.onopen = function () {
            console.log("WS Connected, initiating handshake...");
            statusDiv.textContent = "Bağlandı";
            statusDiv.style.color = "#4CAF50";
            initiateHandshake();
        };

        ws.onclose = function () {
            statusDiv.textContent = "Bağlantı Kesildi";
            statusDiv.style.color = "red";
        };

        ws.getError = function (e) {
            console.log(e);
            statusDiv.textContent = "Hata oluştu";
            statusDiv.style.color = "red";
        };

        ws.onmessage = async function (event) {
            const data = JSON.parse(event.data);
            if (data.type === 'handshake_response') {
                handleHandshakeResponse(data);
            }
        };
    } catch (e) {
        statusDiv.textContent = "Geçersiz URL";
    }
}

async function handleHandshakeResponse(data) {
    try {
        const pubX = BigInt(data.public_key_x);
        const pubY = BigInt(data.public_key_y);


        document.getElementById('server-pub').value = `X: ${data.public_key_x}\nY: ${data.public_key_y}`;

        const xHex = pubX.toString(16).padStart(64, '0');
        const yHex = pubY.toString(16).padStart(64, '0');
        const rawKeyHex = '04' + xHex + yHex;

        const rawKey = hex2buf(rawKeyHex);

        const serverKey = await window.crypto.subtle.importKey(
            "raw",
            rawKey,
            { name: "ECDH", namedCurve: "P-256" },
            false,
            []
        );

        const bits = await window.crypto.subtle.deriveBits(
            { name: "ECDH", public: serverKey },
            localKeyPair.privateKey,
            256
        );

        const hashBuffer = await window.crypto.subtle.digest('SHA-256', bits);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        sharedSecret = hashHex;
        document.getElementById('shared-secret').value = sharedSecret;

        const method = document.getElementById('sifrele-yontem').value;
        if (method === 'aes' || method === 'des') {
            updateKeyHint();
        }

        console.log("Handshake successful. Shared Secret Established.");
    } catch (error) {
        console.error("Handshake failed:", error);
    }
}

async function initiateHandshake() {
    try {
        localKeyPair = await window.crypto.subtle.generateKey(
            { name: "ECDH", namedCurve: "P-256" },
            true,
            ["deriveKey", "deriveBits"]
        );

        const exported = await window.crypto.subtle.exportKey("raw", localKeyPair.publicKey);
        const keyBytes = new Uint8Array(exported);
        const x = BigInt('0x' + buf2hex(keyBytes.slice(1, 33)));
        const y = BigInt('0x' + buf2hex(keyBytes.slice(33, 65)));
        document.getElementById('local-pub').value = `X: ${x.toString()}\nY: ${y.toString()}`;

        ws.send(JSON.stringify({
            type: 'handshake',
            public_key_x: x.toString(),
            public_key_y: y.toString()
        }));
    } catch (e) {
        console.error("Crypto error:", e);
    }
}

function copyToClipboard(elementId) {
    const copyText = document.getElementById(elementId);
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value).then(() => {

        const originalBg = copyText.style.backgroundColor;
        copyText.style.backgroundColor = "#4CAF50";
        setTimeout(() => {
            copyText.style.backgroundColor = originalBg;
        }, 200);
    });
}

async function generateRSAKeys() {
    try {
        const response = await fetch('/generate-rsa-keys');
        const data = await response.json();

        document.getElementById('rsa-pub').value = `${data.public_key[0]},${data.public_key[1]}`;
        document.getElementById('rsa-priv').value = `${data.private_key[0]},${data.private_key[1]}`;

    } catch (e) {
        alert("RSA Anahtar üretimi başarısız: " + e);
    }
}

function buf2hex(buffer) {
    return [...new Uint8Array(buffer)]
        .map(x => x.toString(16).padStart(2, '0'))
        .join('');
}

function hex2buf(hexString) {
    return new Uint8Array(hexString.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
}

document.addEventListener('DOMContentLoaded', function () {
    const methodSelect = document.getElementById('sifrele-yontem');
    methodSelect.addEventListener('change', updateKeyHint);
    updateKeyHint();
    connectWebSocket();

    fetch('/get-server-public-key')
        .then(response => response.json())
        .then(data => {
            if (data.public_key) {
                serverRSAPublicKey = data.public_key.join(',');
                console.log("Sunucu RSA Public Key Alındı:", serverRSAPublicKey);
            }
        })
        .catch(err => console.error("RSA Key fetch failed:", err));
});

function updateKeyHint() {
    const method = document.getElementById('sifrele-yontem').value;
    const keyInput = document.getElementById('anahtar');
    const keyHint = document.getElementById('anahtar-aciklama');

    keyInput.disabled = false;

    if (sharedSecret) {
        if (method === 'aes') {
            keyInput.value = sharedSecret.substring(0, 16);
        } else if (method === 'des') {
            keyInput.value = sharedSecret.substring(0, 8);
        } else {
            keyInput.value = '';
        }
    } else {
        keyInput.value = '';
    }

    switch (method) {
        case 'caesar':
            keyInput.type = 'number';
            keyInput.placeholder = 'Kaydırma sayısı';
            keyHint.textContent = 'Örnek: 3';
            break;
        case 'vigenere':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar kelime';
            keyHint.textContent = 'Örnek: ANAHTAR';
            break;
        case 'substitution':
            keyInput.type = 'text';
            keyInput.placeholder = '26 karakterlik karışık alfabe';
            keyHint.textContent = 'Örnek: QWERTYUIOPASDFGHJKLZXCVBNM';
            break;
        case 'affine':
            keyInput.type = 'text';
            keyInput.placeholder = 'a,b değerleri';
            keyHint.textContent = 'Örnek: 5,8 (a ile 26 aralarında asal olmalı)';
            break;
        case 'playfair':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar kelime';
            keyHint.textContent = 'Örnek: PLAYFAIR';
            break;
        case 'polybius':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar gerekmez';
            keyInput.disabled = true;
            keyHint.textContent = 'Standart Polybius karesi kullanılır';
            break;
        case 'rail_fence':
            keyInput.type = 'number';
            keyInput.placeholder = 'Derinlik (Ray sayısı)';
            keyHint.textContent = 'Örnek: 3';
            break;
        case 'pigpen':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar gerekmez';
            keyInput.disabled = true;
            keyHint.textContent = 'Standart Pigpen şifrelemesi';
            break;
        case 'hill':
            keyInput.type = 'text';
            keyInput.placeholder = '2x2 veya 3x3 matris değerleri girin';
            keyHint.textContent = 'Örnek: 3,3,2,5 (2x2) veya 6,24,1,13,16,10,20,17,15 (3x3)';
            break;
        case 'rotate':
            keyInput.type = 'number';
            keyInput.placeholder = 'Kaydırma sayısını girin (örn: 13)';
            keyHint.textContent = 'ROT-13 için 13 girin';
            break;
        case 'sha1':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar gerekmez';
            keyInput.disabled = true;
            keyHint.textContent = 'SHA-1 hash fonksiyonu - anahtar gerekmez';
            break;
        case 'sha2':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar gerekmez';
            keyInput.disabled = true;
            keyHint.textContent = 'SHA-256 hash fonksiyonu - anahtar gerekmez';
            break;
        case 'aes':
            keyInput.type = 'text';
            keyInput.placeholder = '16 karakterlik anahtar girin';
            keyHint.textContent = 'AES-128 için tam 16 karakter uzunluğunda anahtar gereklidir (Otomatik dağıtılmış)';
            break;
        case 'des':
            keyInput.type = 'text';
            keyInput.placeholder = '8 karakterlik anahtar girin';
            keyHint.textContent = 'DES için tam 8 karakter uzunluğunda anahtar gereklidir (Otomatik dağıtılmış)';
            break;
        case 'route':
            keyInput.type = 'text';
            keyInput.placeholder = 'Satır,Sütun sayısı (örn: 4,5)';
            keyHint.textContent = 'Matris boyutlarını virgülle ayırarak girin';
            break;
        case 'rsa':
            keyInput.type = 'text';
            keyInput.placeholder = 'Public key (e,n) formatında girin';
            keyHint.textContent = 'Örnek: 65537,123456789 - RSA anahtar çifti kullanın';
            break;
        case 'columnar':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar kelimeyi girin';
            keyHint.textContent = 'Sütunları karıştırmak için bir anahtar kelime girin';
            break;
    }

    const noKeyMethods = ['sha1', 'sha2', 'pigpen', 'polybius'];
    if (!noKeyMethods.includes(method)) {
        keyInput.disabled = false;
    }
}

function sifreleVeGonder() {
    const mesaj = document.getElementById('mesaj').value;
    const anahtar = document.getElementById('anahtar').value;
    const yontem = document.getElementById('sifrele-yontem').value;
    const mod = document.getElementById('implementasyon-modu').value;

    const noKeyMethods = ['sha1', 'sha2', 'pigpen', 'polybius'];

    if (!mesaj) {
        alert('Lütfen mesaj girin!');
        return;
    }

    if (!noKeyMethods.includes(yontem) && !anahtar && yontem !== 'rsa') {
        alert('Lütfen anahtar girin!');
        return;
    }

    let cipherText = "";
    let finalKeyToSend = anahtar;
    let isEncrypted = false;
    try {
        if (yontem === 'rsa') {
            const sessionKey = Array.from({ length: 16 }, () => Math.floor(Math.random() * 10).toString()).join('') + 'ABCDEF'.substring(0, 6);
            const actualSessionKey = sessionKey.slice(0, 16);
            if (mod === 'library') {
                const keyBytes = CryptoJS.enc.Utf8.parse(actualSessionKey);
                cipherText = CryptoJS.AES.encrypt(mesaj, keyBytes, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }).toString();
            } else {
                cipherText = ManualAES.encrypt(mesaj, actualSessionKey);
            }
            isEncrypted = true;

            if (!serverRSAPublicKey) {
                alert("Sunucu RSA anahtarı alınamadı! Lütfen sayfayı yenileyin.");
                return;
            }
            finalKeyToSend = ManualRSA.encrypt(actualSessionKey, serverRSAPublicKey);
            console.log("Hybrid RSA: Encrypted Key sent:", finalKeyToSend);
        }
        else if (yontem === 'aes') {
            if (mod === 'library') {
                const keyBytes = CryptoJS.enc.Utf8.parse(anahtar.padEnd(16, '\0').slice(0, 16));
                cipherText = CryptoJS.AES.encrypt(mesaj, keyBytes, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }).toString();
            } else {
                cipherText = ManualAES.encrypt(mesaj, anahtar);
            }
            isEncrypted = true;
        }
        else if (yontem === 'des') {
            // DES uses CryptoJS library for both modes (no manual JS implementation)
            const keyBytes = CryptoJS.enc.Utf8.parse(anahtar.padEnd(8, '\0').slice(0, 8));
            cipherText = CryptoJS.DES.encrypt(mesaj, keyBytes, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }).toString();
            isEncrypted = true;
        }
        else {
            cipherText = mesaj;
            isEncrypted = false;
        }
    } catch (e) {
        console.error(e);
        alert("Şifreleme Hatası: " + e);
        return;
    }

    let actualImplementation = mod;

    const data = {
        method: yontem,
        key: finalKeyToSend,
        message: isEncrypted ? cipherText : mesaj,
        encrypted: isEncrypted,
        implementation: actualImplementation
    };

    ws.send(JSON.stringify(data));
    document.getElementById('mesaj').value = '';

    if (yontem === 'rsa') {
        alert('Mesaj ve Otomatik Oturum Anahtarı (RSA ile) şifrelenip gönderildi!');
    } else {
        alert('Mesaj ' + (isEncrypted ? 'şifrelenip ' : '') + 'gönderildi!');
    }
}

async function dosyaGonder() {
    const fileInput = document.getElementById('dosya-input');
    const file = fileInput.files[0];
    const key = document.getElementById('anahtar').value;
    const method = document.getElementById('sifrele-yontem').value;

    const noKeyMethods = ['sha1', 'sha2', 'pigpen', 'polybius'];

    if (!file) {
        alert("Lütfen bir dosya seçin!");
        return;
    }

    if (!key && !noKeyMethods.includes(method)) {
        alert("Lütfen anahtar girin!");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('method', method);
    formData.append('key', key);

    try {
        const response = await fetch('/send-file', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            alert("Hata: " + result.error);
        } else {
            alert("Dosya şifrelendi ve sunucuya gönderildi!");
            fileInput.value = '';
        }

    } catch (e) {
        console.error(e);
        alert("Dosya gönderme hatası!");
    }
}

async function dosyaDesifreleIndir() {
    const fileInput = document.getElementById('dosya-input');
    const file = fileInput.files[0];
    const key = document.getElementById('anahtar').value;
    const method = document.getElementById('sifrele-yontem').value;

    if (!file) {
        alert("Lütfen şifreli bir dosya seçin!");
        return;
    }

    const noKeyMethods = ['sha1', 'sha2', 'pigpen', 'polybius'];

    if (!key && !noKeyMethods.includes(method)) {
        alert("Lütfen anahtar girin!");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('method', method);
    formData.append('key', key);

    try {
        const response = await fetch('/upload-decrypt', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error("Download failed");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `decrypted_${file.name.replace('encrypted_', '')}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

    } catch (e) {
        console.error(e);
        alert("Dosya deşifreleme hatası!");
    }
}

async function dsaSign() {
    const mesaj = document.getElementById('mesaj').value;
    const statusDiv = document.getElementById('dsa-status');

    if (!mesaj) {
        alert("Lütfen imzalanacak bir mesaj girin!");
        return;
    }

    statusDiv.textContent = "İmzalanıyor...";
    statusDiv.style.color = "yellow";

    try {
        const response = await fetch('/dsa/sign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: mesaj })
        });

        const data = await response.json();

        document.getElementById('dsa-r').value = data.signature_r;
        document.getElementById('dsa-s').value = data.signature_s;

        document.getElementById('dsa-pub-x').value = data.public_key_x;
        document.getElementById('dsa-pub-y').value = data.public_key_y;

        statusDiv.textContent = "Mesaj İmzalandı! (R ve S değerleri alındı)";
        statusDiv.style.color = "#4CAF50";

    } catch (e) {
        console.error(e);
        statusDiv.textContent = "İmzalama Hatası!";
        statusDiv.style.color = "red";
    }
}

async function dsaVerify() {
    const mesaj = document.getElementById('mesaj').value;
    const r = document.getElementById('dsa-r').value;
    const s = document.getElementById('dsa-s').value;
    const pubX = document.getElementById('dsa-pub-x').value;
    const pubY = document.getElementById('dsa-pub-y').value;
    const statusDiv = document.getElementById('dsa-status');

    if (!mesaj || !r || !s) {
        alert("Lütfen mesaj ve imza (r, s) alanlarını doldurun!");
        return;
    }

    statusDiv.textContent = "Doğrulanıyor...";
    statusDiv.style.color = "yellow";

    const payload = {
        message: mesaj,
        signature_r: r,
        signature_s: s
    };
    if (pubX && pubY) {
        payload.public_key_x = pubX;
        payload.public_key_y = pubY;
    }

    try {
        const response = await fetch('/dsa/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        statusDiv.textContent = data.status;
        statusDiv.style.color = data.valid ? "#4CAF50" : "red";

    } catch (e) {
        console.error(e);
        statusDiv.textContent = "Doğrulama sunucu hatası!";
        statusDiv.style.color = "red";
    }
}