document.addEventListener("DOMContentLoaded", function () {
    var scrollingText = document.querySelector(".scrolling-text");
    var copyMessage = document.createElement("div");
    copyMessage.className = "copy-message";
    document.body.appendChild(copyMessage);

    // 从文本文件中读取数据
    function fetchDataFromFile(url) {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                // 将文本内容按中文逗号拆分为数组
                var dataArray = data.split('，');
                createScrollingElements(dataArray);
            })
            .catch(error => console.error('Error fetching data from file:', error));
    }

    // 创建滚动元素
    function createScrollingElements(dataArray) {
        dataArray.forEach(function(item) {
            var span = document.createElement("span");
            span.textContent = item.trim(); // 去除文本前后的空格
            span.classList.add("copy-text");
            span.addEventListener("click", function() {
                var tempInput = document.createElement("input");
                tempInput.value = item.trim();
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand("copy");
                document.body.removeChild(tempInput);
                showCopyMessage();
            });
            scrollingText.appendChild(span);
        });
    }

    function showCopyMessage() {
        copyMessage.textContent = "已复制到粘贴板";
        setTimeout(function() {
            copyMessage.textContent = "";
        }, 2000); // 2秒后隐藏提示消息
    }

    // 从文本文件中获取数据并创建滚动元素
    fetchDataFromFile("/static/datasets/scrolling.txt");

    scrollingText.addEventListener("mouseover", function() {
        this.style.animationPlayState = "paused";
    });

    scrollingText.addEventListener("mouseout", function() {
        this.style.animationPlayState = "running";
    });

    // 如果需要不断循环显示滚动数据，可以使用以下代码
    // setInterval(restartScrollingAnimation, 10000); // 控制滚动数据切换的间隔时间，单位为毫秒
});
