document.addEventListener("DOMContentLoaded", function () {
    var data = ["Scrolling Data 1", "Scrolling Data 2", "Scrolling Data 3"]; // 添加更多滚动数据

    var scrollingText = document.querySelector(".scrolling-text");
    var copyMessage = document.createElement("div");
    copyMessage.className = "copy-message";
    document.body.appendChild(copyMessage);

    function createScrollingElements() {
        data.forEach(function(item) {
            var span = document.createElement("span");
            span.textContent = item;
            span.classList.add("copy-text");
            span.addEventListener("click", function() {
                var tempInput = document.createElement("input");
                tempInput.value = item;
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

    // 创建滚动元素
    createScrollingElements();

    scrollingText.addEventListener("mouseover", function() {
        this.style.animationPlayState = "paused";
    });

    scrollingText.addEventListener("mouseout", function() {
        this.style.animationPlayState = "running";
    });

    // 如果需要不断循环显示滚动数据，可以使用以下代码
    // setInterval(restartScrollingAnimation, 10000); // 控制滚动数据切换的间隔时间，单位为毫秒
});
