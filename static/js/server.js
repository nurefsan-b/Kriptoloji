const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = function (event) {
    console.log("Mesaj alındı:", event.data);
    const data = JSON.parse(event.data);
    const uniqueId = Date.now();
    const mesajDiv = document.createElement('div');
    mesajDiv.className = 'mesaj';

    if (data.type === 'new_file') {
        console.log("Dosya mesajı işleniyor:", data);
        renderFileMessage(mesajDiv, data, uniqueId);
    } else {
        renderTextMessage(mesajDiv, data, uniqueId);
    }

    document.getElementById('mesajlar').prepend(mesajDiv);
};

function renderFileMessage(container, data, uniqueId) {
    container.className = 'mesaj file-message';
    container.innerHTML = `
        <div class="mesaj-header">
            <span class="method-badge">${data.method} - DOSYA</span>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
        <div class="file-content">
            <p><strong>Gelen Dosya:</strong> ${data.original_name}</p>
            <p><strong>Şifreli İsim:</strong> ${data.filename}</p>
            <div class="file-actions" id="actions_${uniqueId}">
                <a href="${data.url}" download="${data.filename}" class="button download-btn">
                    Şifreli İndir
                </a>
                
                <!-- Verification Section -->
                <div style="display: flex; gap: 5px; align-items: center;">
                    <input type="text" id="verify_key_${uniqueId}" placeholder="Anahtarı Doğrula" 
                           style="padding: 5px; width: 120px; font-size: 0.9em;">
                    <button class="button decrypt-btn" onclick="verifyAndDownload('${data.filename}', '${data.method}', '${data.key}', '${uniqueId}')">
                        Doğrula ve İndir
                    </button>
                </div>
            </div>
        </div>
    `;
}

function verifyAndDownload(filename, method, correctKey, uniqueId) {
    const inputKey = document.getElementById(`verify_key_${uniqueId}`).value;

    if (inputKey === correctKey) {
        window.location.href = `/decrypt-download?filename=${filename}&method=${method}&key=${encodeURIComponent(correctKey)}`;

        const btn = document.querySelector(`#actions_${uniqueId} .decrypt-btn`);
        btn.innerHTML = "✓ Doğrulandı";
        btn.style.backgroundColor = "#4CAF50";
    } else {
        alert("Hatalı Anahtar! Lütfen doğru anahtarı girin.");
        document.getElementById(`verify_key_${uniqueId}`).style.borderColor = "red";
    }
}

function renderTextMessage(container, data, uniqueId) {
    const isHash = data.method === 'sha1' || data.method === 'sha2';
    const isRSA = data.method === 'rsa';
    const keyDetails = getKeyInputDetails(data.method);

    let decipherSection = '';
    if (isHash) {
        decipherSection = '<p class="hash-note"><em>Hash tek yönlüdür, deşifre edilemez.</em></p>';
    } else if (isRSA) {
        if (data.decrypted_message) {
            decipherSection = `<p class="decrypted-display" style="background: #2e7d32; color: #fff; padding: 10px; border-radius: 5px; margin-top: 10px;"><strong>Çözülmüş Mesaj:</strong> ${data.decrypted_message}</p>`;
        } else {
            decipherSection = '<p class="rsa-note" style="color: #ff9800;"><em>RSA Hybrid: Çözme bekleniyor...</em></p>';
        }
    } else {
        decipherSection = `
        <div class="decipher-section">
            <input type="${keyDetails.type}" id="key_${uniqueId}" 
                   placeholder="${keyDetails.placeholder}" 
                   class="decipher-input"
                   ${keyDetails.disabled ? 'disabled' : ''}>
            <button class="button" onclick="desifrele('${data.message}', '${data.method}', ${uniqueId}, '${data.implementation || 'manual'}')">
                <img src="/static/images/lock.webp" alt="Kilit İkonu">
                Deşifre Et
            </button>
        </div>
        <small class="key-hint" style="color: #666; font-size: 0.8em; margin-top: 5px; display: block;">${keyDetails.hint}</small>
        <div id="decrypted_${uniqueId}" class="decrypted-message" style="display: none;"></div>
        `;
    }

    container.innerHTML = `
        <div class="mesaj-header">
            <span class="method-badge">${data.method}</span>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
        <p><strong>${isHash ? 'Hash Değeri' : 'Şifreli Mesaj'}:</strong> ${data.message}</p>
        ${data.duration_ms ? `<p class="timing-info">⏱️ İşlem Süresi: ${data.duration_ms} ms</p>` : ''}
        ${decipherSection}
    `;
}

function getKeyInputDetails(method) {
    switch (method) {
        case 'caesar':
            return {
                type: 'number',
                placeholder: 'Kaydırma sayısı',
                hint: 'Örnek: 3'
            };
        case 'vigenere':
            return {
                type: 'text',
                placeholder: 'Anahtar kelime',
                hint: 'Örnek: ANAHTAR'
            };
        case 'substitution':
            return {
                type: 'text',
                placeholder: 'Alfabe sırası',
                hint: '26 karakterlik karışık alfabe'
            };
        case 'affine':
            return {
                type: 'text',
                placeholder: 'a,b değerleri',
                hint: 'Örnek: 5,8'
            };
        case 'playfair':
            return {
                type: 'text',
                placeholder: 'Anahtar kelime',
                hint: 'Örnek: PLAYFAIR'
            };
        case 'polybius':
            return {
                type: 'text',
                placeholder: 'Anahtar gerekmez',
                hint: 'Standart tablo kullanılır',
                disabled: true
            };
        case 'rail_fence':
            return {
                type: 'number',
                placeholder: 'Derinlik',
                hint: 'Örnek: 3'
            };
        case 'pigpen':
            return {
                type: 'text',
                placeholder: 'Anahtar gerekmez',
                hint: 'Standart desen kullanılır',
                disabled: true
            };
        case 'hill':
            return {
                type: 'text',
                placeholder: 'Matris değerleri',
                hint: 'Örnek: 3,3,2,5 (2x2) veya 6,24,1,13,16,10,20,17,15 (3x3)'
            };
        case 'rotate':
            return {
                type: 'number',
                placeholder: 'Kaydırma sayısı (örn: 3)',
                hint: 'Pozitif bir tam sayı girin'
            };
        case 'aes':
            return {
                type: 'text',
                placeholder: '16 karakterlik anahtar',
                hint: 'AES-128 için tam 16 karakter'
            };
        case 'des':
            return {
                type: 'text',
                placeholder: '8 karakterlik anahtar',
                hint: 'DES için tam 8 karakter'
            };
        case 'route':
            return {
                type: 'text',
                placeholder: 'Satır,Sütun (örn: 4,5)',
                hint: 'Matris boyutlarını virgülle ayırarak girin'
            };
        case 'rsa':
            return {
                type: 'text',
                placeholder: 'Private key (d,n)',
                hint: 'Örnek: 2753,3233 (d ve n virgülle ayrılmış)'
            };
        case 'columnar':
            return {
                type: 'text',
                placeholder: 'Anahtar kelime',
                hint: 'Sütunları karıştırmak için kullanılan anahtar kelime'
            };
        default:
            return {
                type: 'text',
                placeholder: 'Deşifreleme anahtarı',
                hint: ''
            };
    }
}

async function desifrele(encryptedMessage, method, uniqueId, implementation = 'manual') {
    try {
        const key = document.getElementById(`key_${uniqueId}`).value;
        const noKeyMethods = ['sha1', 'sha2', 'pigpen', 'polybius'];

        if (!key && !noKeyMethods.includes(method)) {
            alert('Lütfen deşifreleme anahtarını girin!');
            return;
        }

        const response = await fetch(`/decrypt?method=${method}&cipher_text=${encodeURIComponent(encryptedMessage)}&key=${encodeURIComponent(key)}&implementation=${implementation}`);
        const result = await response.json();

        if (result.error) {
            alert('Deşifreleme hatası: ' + result.error);
            return;
        }

        const decryptedDiv = document.getElementById(`decrypted_${uniqueId}`);
        decryptedDiv.innerHTML = `
            <p class="success">Deşifreleme Başarılı!</p>
            <p><strong>Deşifrelenmiş Mesaj:</strong> ${result.decrypted_message}</p>
            ${result.duration_ms ? `<p class="timing-info">⏱️ Deşifre Süresi: ${result.duration_ms} ms</p>` : ''}
        `;
        decryptedDiv.style.display = 'block';
    } catch (error) {
        console.error('Deşifreleme hatası:', error);
        alert('Deşifreleme sırasında bir hata oluştu!');
    }
}