



document.addEventListener('DOMContentLoaded', () => {
    const dicomCanvas = document.getElementById("dicomCanvas");
    const dicomImage = document.getElementById("dicomImage");
    const ctx = dicomCanvas.getContext('2d');
    const fileId = dicomImage.getAttribute('data-file-id');
    const histogramCanvas = document.getElementById('histogram');
    let graph = null;



    function stampImage() {
        dicomCanvas.width = dicomImage.naturalWidth;
        dicomCanvas.height = dicomImage.naturalHeight;

        ctx.drawImage(dicomImage, 0, 0);
    }

    if (dicomImage.complete && dicomImage.naturalWidth !== 0) {
        stampImage()
    }
    else {
        dicomImage.addEventListener("load", stampImage)
    }

    async function applyFilter(filterType, extraData = {}) {
        const payload = { "filter": filterType, ...extraData };
        const response = await fetch(`/api/process/${fileId}`, {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify(payload)
        });

        const blb = await response.blob()

        const tempUrl = URL.createObjectURL(blb);

        const img = new Image();

        img.onload = () => {
            ctx.clearRect(0, 0, dicomCanvas.width, dicomCanvas.height);
            ctx.drawImage(img, 0, 0);
            URL.revokeObjectURL(tempUrl);
        }

        img.src = tempUrl;
        fetchAndDrawHisogram();
    }


    document.querySelectorAll(".toolbar button").forEach(button => {
        button.addEventListener("click", (event) => {
            const filterName = event.target.getAttribute('data-filter');

            if (filterName) {
                applyFilter(filterName);
            }
        })
    });


    let isDraging = false;
    let startX = 0;
    let startY = 0
    let currentWindow = 400;
    let currentLevel = 40;


    dicomCanvas.addEventListener('mousedown', (event) => {
        isDraging = true;
        startX = event.clientX;
        startY = event.clientY;
    })

    dicomCanvas.addEventListener('mousemove', (event) => {
        if (!isDraging) {
            return;
        }

        const deltaX = event.clientX - startX;
        const deltaY = event.clientY - startY;
        currentWindow += deltaX * 2;
        currentLevel -= deltaY * 2;
        if (currentWindow < 1) {
            currentWindow = 1;
        }
        startX = event.clientX;
        startY = event.clientY;

    });

    dicomCanvas.addEventListener('mouseup', (event) => {
        if (isDraging) {
            isDraging = false;
            applyFilter('window', { window: currentWindow, level: currentLevel });
        }

    });

    async function fetchAndDrawHisogram() {
        const hist = await fetch(`/api/histogram/${fileId}`);
        const data = await hist.json();
        const arr = data.histogram;
        const histogramctx = histogramCanvas.getContext('2d');

        const xLabel = Array.from({ length: 256 }, (_, i) => i);
        if (graph) {
            graph.destroy();
        }
        graph = new Chart(histogramctx, {
            type: "bar",
            data: {
                labels: xLabel,
                datasets: [{
                    label: "Graph",
                    data: arr,
                    backgroundColor: "rgba(75, 192, 192, 0.6)"
                }]

            },
            options: {
                animation: false
            }
        });
    }
    fetchAndDrawHisogram();


    const btnAi = document.getElementById('btn-ai-analyze');
    const aiReportBox = document.getElementById('ai-report-box');
    const aiReportText = document.getElementById('ai-report-text');

    if (btnAi) {
        btnAi.addEventListener('click', async () => {
            // Змінюємо стан кнопки на "завантаження"
            btnAi.innerText = '⏳ AI is scanning tissue...';
            btnAi.disabled = true;

            // Показуємо чорний екран звіту з текстом завантаження
            aiReportBox.style.display = 'block';
            aiReportText.innerText = 'Transmitting image matrix to Gemini servers...\nWaiting for radiological analysis...';

            try {
                // Звертаємося до твого нового бекенд-маршруту
                const response = await fetch(`/api/report/${fileId}`);
                const data = await response.json();

                // Вставляємо фінальний звіт на екран
                aiReportText.innerText = data.report;

            } catch (error) {
                aiReportText.innerText = "Error connecting to AI Backend: " + error;
            } finally {
                // Повертаємо кнопку в нормальний стан
                btnAi.innerText = '🤖 Re-run AI Analysis';
                btnAi.disabled = false;
            }
        });
    }




});


