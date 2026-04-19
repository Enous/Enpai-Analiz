const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs-extra');

function createWindow() {
    const win = new BrowserWindow({
        width: 1280,
        height: 950,
        frame: false,
        icon: path.join(__dirname, 'assets', 'icon.png'),
        backgroundColor: '#08080A',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

// IPC Handlers
ipcMain.handle('select-dirs', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openDirectory']
    });
    return result.filePaths[0];
});

ipcMain.handle('scan-files', async (event, srcPath) => {
    try {
        const files = await fs.readdir(srcPath);
        const results = [];
        for (const file of files) {
            const fullPath = path.join(srcPath, file);
            const stats = await fs.stat(fullPath);
            if (stats.isFile()) {
                results.push({
                    name: file,
                    size: (stats.size / (1024 * 1024)).toFixed(2) + ' MB',
                    ext: path.extname(file).toLowerCase()
                });
            }
        }
        return results;
    } catch (err) {
        return [];
    }
});

ipcMain.on('process-files', async (event, { files, src, dst, op }) => {
    let count = 0;
    let lastPercent = -1;
    const baseTargetDir = path.join(dst, 'Enpai-Dev Analiz');
    await fs.ensureDir(baseTargetDir);

    for (const file of files) {
        const category = getCategory(file.ext, file.name);
        const targetDir = path.join(baseTargetDir, category);
        await fs.ensureDir(targetDir);
        
        const srcFile = path.join(src, file.name);
        const dstFile = path.join(targetDir, file.name);

        try {
            if (op === 'move') {
                await fs.move(srcFile, dstFile, { overwrite: false });
            } else {
                await fs.copy(srcFile, dstFile);
            }
        } catch (e) {
            console.error(e);
        }
        
        count++;
        const percent = Math.floor((count / files.length) * 100);
        if (percent !== lastPercent) {
            lastPercent = percent;
            event.reply('progress', (count / files.length));
        }
    }
    event.reply('done');
});

const CATEGORIES = {
    "Kodlama": [".py", ".js", ".cpp", ".h", ".java", ".html", ".css", ".ts", ".go", ".rs", ".php", ".sql", ".au3", ".ipynb", ".c", ".cs"],
    "Oyun": [".exe", ".msi", ".iso", ".pak", ".vpk", ".rpf", ".bin", ".dat"],
    "Arşiv": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Medya": [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".mp4", ".mkv", ".mov", ".avi", ".mp3", ".wav", ".flac"],
    "Belgeler": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "3D_Tasarım": [".stl", ".obj", ".fbx", ".3ds", ".dae"]
};

function getCategory(ext, name) {
    for (const [cat, exts] of Object.entries(CATEGORIES)) {
        if (exts.includes(ext)) return cat;
    }
    const keywords = ["setup", "game", "crack", "repack", "fitgirl", "dodi", "steam", "launcher"];
    if (keywords.some(kw => name.toLowerCase().includes(kw))) return "Oyun";
    return "Diğer";
}

ipcMain.on('close-app', () => app.quit());
