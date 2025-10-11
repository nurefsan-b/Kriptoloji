const ws = new WebSocket(`ws://${window.location.host}/ws`);
    
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const uniqueId = Date.now();
    const mesajDiv = document.createElement('div');
    mesajDiv.className = 'mesaj';
    mesajDiv.innerHTML = `
        <div class="mesaj-header">
            <span class="method-badge">${data.method}</span>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>
        <p><strong>Şifreli Mesaj:</strong> ${data.encrypted_message}</p>
        <div class="decipher-section">
            <input type="text" id="key_${uniqueId}" 
                   placeholder="Deşifreleme anahtarını girin" 
                   class="decipher-input">
            <button class="button" onclick="desifrele('${data.encrypted_message}', '${data.method}', ${uniqueId})">
                <img src="/static/images/lock.webp" alt="Kilit İkonu">
                Deşifre Et
            </button>
        </div>
        <div id="decrypted_${uniqueId}" class="decrypted-message" style="display: none;"></div>
    `;
    
    document.getElementById('mesajlar').prepend(mesajDiv);
};

async function desifrele(encryptedMessage, method, uniqueId) {
    try {
        const key = document.getElementById(`key_${uniqueId}`).value;
        if (!key) {
            alert('Lütfen deşifreleme anahtarını girin!');
            return;
        }

        const response = await fetch(`/decrypt?method=${method}&cipher_text=${encryptedMessage}&key=${key}`);
        const result = await response.json();
        
        if (result.error) {
            alert('Deşifreleme hatası: ' + result.error);
            return;
        }

        const decryptedDiv = document.getElementById(`decrypted_${uniqueId}`);
        decryptedDiv.innerHTML = `
            <p class="success">Deşifreleme Başarılı!</p>
            <p><strong>Deşifrelenmiş Mesaj:</strong> ${result.decrypted_message}</p>
        `;
        decryptedDiv.style.display = 'block';
    } catch (error) {
        console.error('Deşifreleme hatası:', error);
        alert('Deşifreleme sırasında bir hata oluştu!');
    }
}