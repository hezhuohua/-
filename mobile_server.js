const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 获取本机IP地址
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const interface of interfaces[name]) {
            if (interface.family === 'IPv4' && !interface.internal) {
                return interface.address;
            }
        }
    }
    return '127.0.0.1';
}

// MIME类型映射
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
};

const server = http.createServer((req, res) => {
    // 设置CORS头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', '*');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    let filePath = '.' + req.url;
    if (filePath === './') {
        filePath = './index.html';
    }
    
    const extname = String(path.extname(filePath)).toLowerCase();
    const mimeType = mimeTypes[extname] || 'application/octet-stream';
    
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                // 404 - 重定向到主页
                fs.readFile('./index.html', (error, content) => {
                    if (error) {
                        res.writeHead(500);
                        res.end('服务器错误');
                    } else {
                        res.writeHead(200, { 'Content-Type': 'text/html' });
                        res.end(content, 'utf-8');
                    }
                });
            } else {
                res.writeHead(500);
                res.end('服务器错误: ' + error.code);
            }
        } else {
            res.writeHead(200, { 'Content-Type': mimeType });
            res.end(content, 'utf-8');
        }
    });
});

const PORT = process.env.PORT || 8080;
const localIP = getLocalIP();

server.listen(PORT, () => {
    console.log('🚀 永续合约预测系统移动端服务器启动成功！');
    console.log('=' .repeat(60));
    console.log(`📱 本机访问地址：http://localhost:${PORT}`);
    console.log(`📱 手机访问地址：http://${localIP}:${PORT}`);
    console.log('=' .repeat(60));
    console.log('📋 使用说明：');
    console.log('1. 确保手机和电脑连接同一个WiFi');
    console.log('2. 在手机浏览器输入上面的手机访问地址');
    console.log('3. 其他人也可以用这个地址访问');
    console.log('4. 按 Ctrl+C 停止服务器');
    console.log('=' .repeat(60));
    console.log(`🌐 服务器运行在端口 ${PORT}...`);
});

// 优雅关闭
process.on('SIGINT', () => {
    console.log('\n👋 服务器已停止');
    process.exit(0);
});
