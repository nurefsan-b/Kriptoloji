const ws = new WebSocket(`ws://${window.location.host}/ws`);

document.addEventListener('DOMContentLoaded', function() {
    const methodSelect = document.getElementById('sifrele-yontem');
    methodSelect.addEventListener('change', updateKeyHint);
    updateKeyHint();
});

function updateKeyHint() {
    const method = document.getElementById('sifrele-yontem').value;
    const keyInput = document.getElementById('anahtar');
    const keyHint = document.getElementById('anahtar-aciklama');
    
    switch(method) {
        case 'caesar':
            keyInput.type = 'number';
            keyInput.placeholder = 'Kaydırma sayısını girin (örn: 3)';
            keyHint.textContent = 'Pozitif bir tam sayı girin';
            break;
        case 'vigenere':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar kelimeyi girin';
            keyHint.textContent = 'Sadece harflerden oluşan bir kelime girin';
            break;
        case 'substitution':
            keyInput.type = 'text';
            keyInput.placeholder = '26 harflik permütasyon girin';
            keyHint.textContent = 'Örnek: QWERTYUIOPASDFGHJKLZXCVBNM';
            break;
        case 'affine':
            keyInput.type = 'text';
            keyInput.placeholder = 'a,b şeklinde iki sayı girin';
            keyHint.textContent = 'Örnek: 5,8 (a ve b sayıları virgülle ayrılmış)';
            break;
        case 'playfair':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar kelimeyi girin';
            keyHint.textContent = 'Sadece harflerden oluşan bir kelime girin';
            break;
        case 'polybius':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar gerekmez (Sabit 5x5)';
            keyInput.disabled = true; 
            keyHint.textContent = 'Standart 5x5 tablo kullanılır (J=I)';
            break;
        case 'rail_fence':
            keyInput.type = 'number';
            keyInput.placeholder = 'Ray (Satır) sayısını girin (örn: 3)';
            keyHint.textContent = 'En az 2 olmalıdır.';
            break;
            
        case 'pigpen':
            keyInput.type = 'text';
            keyInput.placeholder = 'Anahtar gerekmez';
            keyInput.disabled = true;
            keyHint.textContent = 'Grafiksel Mason şifresi kullanılır.';
            break;
        }
}

function sifreleVeGonder() {
    const mesaj = document.getElementById('mesaj').value;
    const anahtar = document.getElementById('anahtar').value;
    const yontem = document.getElementById('sifrele-yontem').value;
    
    if (!mesaj || (!anahtar && yontem !== 'polybius' && yontem !== 'pigpen')) {
        alert('Lütfen mesaj ve (bu yöntem için gerekliyse) anahtar girin!');
        return;
    }

    const data = {
        method: yontem,
        key: anahtar || "0", 
        message: mesaj,
        encrypted: true
    };
    
    ws.send(JSON.stringify(data));
    document.getElementById('mesaj').value = '';
    document.getElementById('anahtar').value = '';
    alert('Mesaj gönderildi!');
}