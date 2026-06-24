



document.addEventListener('DOMContentLoaded', () => {
    dicomCanvas = document.getElementById("dicomCanvas")
    dicomImage = document.getElementById("dicomImage")
    ctx = dicomCanvas.getContext('2d')
    fileId = dicomImage.getAttribute('data-file-id')


    function stampImage() {
        dicomCanvas.width = dicomImage.naturalWidth;
        dicomCanvas.height = dicomImage.naturalHeight

        ctx.drawImage(dicomImage, 0, 0)
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


});


