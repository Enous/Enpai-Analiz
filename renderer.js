const { ipcRenderer } = require('electron');

const srcInput = document.getElementById('src-path');
const dstInput = document.getElementById('dst-path');
const fileList = document.getElementById('file-list');
const scanBtn = document.getElementById('scan-btn');
const processBtn = document.getElementById('process-btn');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');

let scannedFiles = [];

// Browse Source
document.getElementById('browse-src').addEventListener('click', async () => {
    const path = await ipcRenderer.invoke('select-dirs');
    if (path) srcInput.value = path;
});

// Browse Destination
document.getElementById('browse-dst').addEventListener('click', async () => {
    const path = await ipcRenderer.invoke('select-dirs');
    if (path) dstInput.value = path;
});

// Close
document.getElementById('close-btn').addEventListener('click', () => {
    ipcRenderer.send('close-app');
});

// Scan
scanBtn.addEventListener('click', async () => {
    const src = srcInput.value;
    if (!src) return alert('Lütfen kaynak klasörü seçin.');

    scanBtn.disabled = true;
    scanBtn.innerText = 'TANIYORUM...';
    
    scannedFiles = await ipcRenderer.invoke('scan-files', src);
    renderFileList(scannedFiles);
    
    scanBtn.disabled = false;
    scanBtn.innerText = 'DOSYALARI ANALİZ ET';
    processBtn.disabled = scannedFiles.length === 0;
});

// Process
processBtn.addEventListener('click', () => {
    const src = srcInput.value;
    const dst = dstInput.value;
    const op = document.querySelector('input[name="op"]:checked').value;

    if (!dst) return alert('Lütfen hedef klasörü seçin.');

    processBtn.disabled = true;
    scanBtn.disabled = true;
    
    ipcRenderer.send('process-files', { files: scannedFiles, src, dst, op });
});

// Progress
ipcRenderer.on('progress', (event, val) => {
    const percent = Math.round(val * 100);
    progressFill.style.width = percent + '%';
    progressText.innerText = percent + '%';
});

ipcRenderer.on('done', () => {
    alert('İşlem Başarıyla Tamamlandı!');
    processBtn.disabled = false;
    scanBtn.disabled = false;
    progressFill.style.width = '0%';
    progressText.innerText = '0%';
    fileList.innerHTML = '<div class="placeholder">İşlem Tamamlandı.</div>';
    scannedFiles = [];
});

function renderFileList(files) {
    fileList.innerHTML = '';
    if (files.length === 0) {
        fileList.innerHTML = '<div class="placeholder">Dosya bulunamadı.</div>';
        return;
    }

    files.forEach(file => {
        const item = document.createElement('div');
        item.className = 'file-item';
        
        const category = getCategory(file.ext, file.name);
        const color = getCategoryColor(category);

        item.innerHTML = `
            <div class="cat-pill" style="background: ${color}">${category}</div>
            <div class="file-details">
                <div class="file-name">${file.name}</div>
                <div class="file-size">${file.size}</div>
            </div>
        `;
        fileList.appendChild(item);
    });
}

function getCategory(ext, name) {
    const CATEGORIES = {
        "Kodlama": [".py", ".js", ".cpp", ".h", ".java", ".html", ".css", ".ts", ".go", ".rs", ".php", ".sql", ".au3", ".ipynb", ".c", ".cs"],
        "Oyun": [".exe", ".msi", ".iso", ".pak", ".vpk", ".rpf", ".bin", ".dat"],
        "Arşiv": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Medya": [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".mp4", ".mkv", ".mov", ".avi", ".mp3", ".wav", ".flac"],
        "Belgeler": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
        "3D_Tasarım": [".stl", ".obj", ".fbx", ".3ds", ".dae"]
    };
    for (const [cat, exts] of Object.entries(CATEGORIES)) {
        if (exts.includes(ext)) return cat;
    }
    const keywords = ["setup", "game", "crack", "repack", "fitgirl", "dodi", "steam", "launcher"];
    if (keywords.some(kw => name.toLowerCase().includes(kw))) return "Oyun";
    return "Diğer";
}

function getCategoryColor(cat) {
    const COLORS = {
        "Kodlama": "#7F00FF",
        "Oyun": "#FF4444",
        "Arşiv": "#FFBB00",
        "Medya": "#00CCFF",
        "Belgeler": "#00FF66",
        "3D_Tasarım": "#FF00FF",
        "Diğer": "#888888"
    };
    return COLORS[cat] || "#888888";
}
