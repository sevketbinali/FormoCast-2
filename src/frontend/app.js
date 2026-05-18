document.addEventListener('DOMContentLoaded', async () => {
    const tickerList = document.getElementById('tickerList');
    const currentTickerTitle = document.getElementById('currentTickerTitle');
    const loader = document.getElementById('loader');
    const chartContainer = document.getElementById('chartContainer');
    const patternsList = document.getElementById('patternsList');
    const patternDetails = document.getElementById('patternDetails');

    // Detay elementleri
    const pType = document.getElementById('pType');
    const pDate = document.getElementById('pDate');
    const pPrice = document.getElementById('pPrice');
    const pDirection = document.getElementById('pDirection');
    const pTargetPrice = document.getElementById('pTargetPrice');
    const pTargetDate = document.getElementById('pTargetDate');

    let chart = null;
    let candleSeries = null;
    let markersSeries = null;
    let currentData = null;

    // 1. Sayfa yüklendiğinde hisse listesini çek
    try {
        const res = await fetch('/api/tickers');
        const data = await res.json();
        if(data.status === 'success') {
            tickerList.innerHTML = '';
            data.data.forEach((ticker, index) => {
                const li = document.createElement('li');
                li.textContent = ticker;
                li.onclick = () => loadTickerHistory(ticker, li);
                tickerList.appendChild(li);

                // İlk hisseyi otomatik yükle
                if(index === 0) {
                    loadTickerHistory(ticker, li);
                }
            });
        }
    } catch (e) {
        tickerList.innerHTML = '<li class="loading-text">Hisseler yüklenemedi.</li>';
    }

    // 2. Hisse verilerini ve 20 yıllık formasyonları çek
    async function loadTickerHistory(ticker, liElement) {
        // Aktif sınıfını güncelle
        document.querySelectorAll('.ticker-list li').forEach(el => el.classList.remove('active'));
        if(liElement) liElement.classList.add('active');

        currentTickerTitle.textContent = `${ticker} - Analiz Yükleniyor...`;
        loader.style.display = 'block';
        patternDetails.style.display = 'none';
        patternsList.innerHTML = '';

        try {
            const res = await fetch(`/api/history/${ticker}`);
            const data = await res.json();

            if (data.status === 'success') {
                currentTickerTitle.textContent = `${ticker} - 20 Yıllık Formasyon Analizi`;
                currentData = data;
                renderChart(data.candles, data.patterns);
                renderPatternsList(data.patterns);
            } else {
                currentTickerTitle.textContent = `${ticker} - Veri Bulunamadı`;
            }
        } catch (e) {
            console.error("Dashboard yüklenirken hata:", e);
            currentTickerTitle.textContent = `Hata Oluştu! ${e.message}`;
            const errDetails = document.createElement('div');
            errDetails.style.color = "red";
            errDetails.style.fontSize = "12px";
            errDetails.style.marginTop = "10px";
            errDetails.textContent = e.stack;
            currentTickerTitle.parentNode.appendChild(errDetails);
        } finally {
            loader.style.display = 'none';
        }
    }

    // 3. Grafiği Çiz (Lightweight Charts)
    function renderChart(candles, patterns) {
        if (!chart) {
            chart = LightweightCharts.createChart(chartContainer, {
                layout: {
                    background: { type: 'solid', color: 'transparent' },
                    textColor: '#d1d5db',
                },
                grid: {
                    vertLines: { color: 'rgba(255, 255, 255, 0.05)' },
                    horzLines: { color: 'rgba(255, 255, 255, 0.05)' },
                },
                crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
                timeScale: { borderColor: 'rgba(255, 255, 255, 0.1)' },
            });
            candleSeries = chart.addCandlestickSeries({
                upColor: '#10b981', downColor: '#ef4444', 
                borderVisible: false, wickUpColor: '#10b981', wickDownColor: '#ef4444'
            });
        }

        candleSeries.setData(candles);

        // Markerları (Formasyon İşaretleri) ekle
        const markersMap = {};
        patterns.forEach(p => {
            const timeStr = p.detection_date;
            if (!markersMap[timeStr]) {
                markersMap[timeStr] = {
                    time: timeStr,
                    position: p.direction === 'YÜKSELİŞ' ? 'belowBar' : 'aboveBar',
                    color: p.direction === 'YÜKSELİŞ' ? '#10b981' : '#ef4444',
                    shape: p.direction === 'YÜKSELİŞ' ? 'arrowUp' : 'arrowDown',
                    text: p.type
                };
            } else {
                // Eğer aynı gün birden fazla formasyon varsa metni birleştir
                markersMap[timeStr].text += ` & ${p.type}`;
            }
        });
        
        const markers = Object.values(markersMap);
        
        // Tarihe göre sıralanmalı
        markers.sort((a, b) => new Date(a.time) - new Date(b.time));
        
        try {
            candleSeries.setMarkers(markers);
        } catch(e) {
            console.error("Marker Hatası:", e);
        }
        chart.timeScale().fitContent();
    }

    // 4. Formasyon Listesini Oluştur
    function renderPatternsList(patterns) {
        if (patterns.length === 0) {
            patternsList.innerHTML = '<div style="color:#94a3b8; font-size: 0.9rem;">Son 20 yılda formasyon tespit edilemedi.</div>';
            return;
        }

        // En yeniden eskiye sırala
        patterns.sort((a, b) => new Date(b.detection_date) - new Date(a.detection_date));

        patterns.forEach((p, idx) => {
            const card = document.createElement('div');
            card.className = 'pattern-card';
            card.innerHTML = `
                <div class="pattern-card-title">
                    <span>${p.type}</span>
                    <span class="direction-badge ${p.direction}">${p.direction}</span>
                </div>
                <div class="pattern-card-date">Oluşum: ${p.detection_date}</div>
            `;

            card.onclick = () => showPatternDetails(p, card);
            patternsList.appendChild(card);
        });
    }

    // 5. Tıklanan formasyonun detaylarını göster ve grafiği oraya kaydır
    function showPatternDetails(p, cardElement) {
        document.querySelectorAll('.pattern-card').forEach(c => c.classList.remove('selected'));
        if (cardElement) cardElement.classList.add('selected');

        patternDetails.style.display = 'block';
        pType.textContent = p.type;
        pDate.textContent = p.detection_date;
        pPrice.textContent = p.detection_price.toFixed(2) + ' TL';
        
        pDirection.textContent = p.direction;
        pDirection.className = p.direction === 'YÜKSELİŞ' ? 'text-success' : 'text-danger';
        pDirection.style.color = p.direction === 'YÜKSELİŞ' ? '#10b981' : '#ef4444';
        
        pTargetPrice.textContent = p.target_price.toFixed(2) + ' TL';
        pTargetDate.textContent = p.target_date;

        // Grafikte formasyonun olduğu tarihe odaklan
        chart.timeScale().setVisibleLogicalRange({
            from: chart.timeScale().coordinateToLogical(0), // Dummy to wake it up
            to: chart.timeScale().coordinateToLogical(1)
        }); // Biraz hacky ama chart objesine zoom yapıyoruz
        
        // Asıl focus:
        // Sadece marker tarihlerini görebilmek için:
        // Lightweight charts'da zaman skalasını belirli bir aralığa set edebiliriz.
        // Ancak en basit yol, veride o tarihi bulup range belirlemektir.
        
        const dataIndex = currentData.candles.findIndex(c => c.time === p.detection_date);
        if(dataIndex !== -1) {
            chart.timeScale().setVisibleLogicalRange({
                from: dataIndex - 30,
                to: dataIndex + 30
            });
        }
    }
});
