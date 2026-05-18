document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scanBtn');
    const btnText = scanBtn.querySelector('.btn-text');
    const btnLoader = scanBtn.querySelector('.btn-loader');
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    const cardsGrid = document.getElementById('cardsGrid');

    scanBtn.addEventListener('click', async () => {
        // UI Güncellemesi: Yükleniyor durumu
        scanBtn.disabled = true;
        btnText.textContent = 'Taranıyor...';
        btnLoader.style.display = 'inline-block';
        statusDot.className = 'dot active';
        statusText.textContent = 'Piyasa canlı olarak taranıyor, geçmiş veriler analiz ediliyor...';
        cardsGrid.innerHTML = ''; // Eski sonuçları temizle

        try {
            const response = await fetch('/api/scan');
            const data = await response.json();

            if (data.status === 'success') {
                const reports = data.data;
                
                if (reports.length === 0) {
                    statusDot.className = 'dot';
                    statusText.textContent = 'Tarama tamamlandı. Şu an için aktif formasyon bulunamadı.';
                } else {
                    statusDot.className = 'dot success';
                    statusText.textContent = `Tarama tamamlandı. ${reports.length} adet fırsat/sinyal bulundu.`;
                    
                    reports.forEach((report, index) => {
                        const card = createCard(report, index);
                        cardsGrid.appendChild(card);
                    });
                }
            } else {
                throw new Error('API Hatası');
            }
        } catch (error) {
            console.error('Tarama hatası:', error);
            statusDot.className = 'dot error';
            statusText.textContent = 'Tarama sırasında bir hata oluştu. Sunucu bağlantısını kontrol edin.';
        } finally {
            // UI Güncellemesi: İşlem bitti
            scanBtn.disabled = false;
            btnText.textContent = 'Yeniden Tara';
            btnLoader.style.display = 'none';
        }
    });

    function createCard(data, index) {
        const card = document.createElement('div');
        card.className = 'signal-card';
        card.style.animationDelay = `${index * 0.1}s`;

        // Yöne göre ikon
        const dirIcon = data.direction === 'YÜKSELİŞ' ? '📈' : '📉';

        card.innerHTML = `
            <div class="card-header">
                <div class="ticker-name">${data.ticker}</div>
                <div class="direction-badge ${data.direction}">${dirIcon} ${data.direction}</div>
            </div>
            <div class="card-body">
                <div class="pattern-name">🔍 Formasyon: ${data.pattern}</div>
                <div class="win-rate">🎯 Geçmiş Başarı: <strong>%${data.win_rate.toFixed(2)}</strong></div>
                <div class="report-text">
                    ${data.report}
                </div>
            </div>
            <div class="card-footer">
                Tespit Tarihi: ${data.date}
            </div>
        `;
        return card;
    }
});
