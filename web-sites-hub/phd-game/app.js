const express = require('express');

let port = 9001;
let app = express();

// 提供 dist 目录下的文件
app.use(express.static('./dist'));

// 提供 static 目录下的文件，支持 /static 路径
app.use('/static', express.static('./static'));

app.listen(port, () => {
    console.log(`Server started on port ${port}.\nPlease navigate to http://localhost:${port} in your browser.`)
});
