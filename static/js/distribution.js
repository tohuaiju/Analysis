$(document).ready(function(){
    // 当页面加载完成时执行以下代码

    // 当搜索框被聚焦时
    $("#search").focus(function() {
        // 添加搜索框的边框样式
        $(".search-box").addClass("border-searching");
        // 添加搜索图标的旋转效果
        $(".search-icon").addClass("si-rotate");
    });

    // 当搜索框失去焦点时
    $("#search").blur(function() {
        // 移除搜索框的边框样式
        $(".search-box").removeClass("border-searching");
        // 移除搜索图标的旋转效果
        $(".search-icon").removeClass("si-rotate");
    });

    // 当在搜索框中按键时
    $("#search").keyup(function(event) {
        // 如果按下的键是回车键
        if(event.key === "Enter"){
            // 触发搜索功能
            searchFunction();
        }
        // 如果搜索框中有文字输入
        else if($(this).val().length > 0) {
            // 添加前往图标的动画效果
            $(".go-icon").addClass("go-in");
        }
        else {
            // 移除前往图标的动画效果
            $(".go-icon").removeClass("go-in");
        }
    });

    $(".go-icon").click(searchFunction);

    function searchFunction(){
        // 获取搜索框的值
        var searchValue = $("#search").val().trim();
        // 加载地图数据并初始化地图
        fetch('static/datasets/maps_china.json')
            .then(response => response.json())
            .then(function(data) {
                // 查找匹配的地图数据
                var matchedData = data[searchValue];

                // 如果找到匹配的地图数据
                if (matchedData) {
                    var overlay = $("<div class='overlay'></div>");
                    $("body").append(overlay);

                    // 创建卡片
                    var card = $("<div class='card'></div>");
                    overlay.append(card);

                    // 创建地图容器并添加到卡片中
                    var mapContainer = $("<div id='chinaMap'></div>");
                    card.append(mapContainer);

                    // 创建中国地图
                    var chinaChart = echarts.init(mapContainer[0]);

                    // 配置地图标题，包含搜索框的值
                    var mapTitle = searchValue + '的分布可视化';

                    // 配置地图选项
                    var chinaOption = {
                        title: {
                            text: mapTitle,
                            left: 'center',
                            top: 30,
                            textStyle: {
                                color: '#fff',
                                fontSize: 16
                            }
                        },
                        tooltip: {
                            trigger: 'item'
                        },
                        series: [
                            {
                                name: '高亮省份',
                                type: 'map',
                                map: 'china', // 使用中国地图
                                roam: true,
                                label: {
                                    show: true,
                                    fontSize: 12
                                },
                                data: matchedData // 设置匹配的地图数据
                            }
                        ]
                    };
                    chinaChart.setOption(chinaOption);

                    // 点击卡片周围时，卡片消失
                    overlay.click(function() {
                        overlay.remove();
                    });
                } else {
                    alert("未找到匹配的地图数据！");
                }
            })
            .catch(function(error) {
                console.error('加载地图数据时发生错误:', error);
            });
    }
});

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
                var dataArray = data.split(',');
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
        // 创建滚动动画
        var animationDuration = scrollingText.scrollWidth / 50; // 根据内容长度动态计算滚动时间
        scrollingText.style.animation = `scrollLeft ${animationDuration}s linear infinite`;
    }

    function showCopyMessage() {
        var notificationContainer = document.querySelector(".notification-container");
        notificationContainer.textContent = "内容已复制到粘贴板";
        notificationContainer.style.display = "block"; // 显示容器

        setTimeout(function() {
            notificationContainer.textContent = "";
            notificationContainer.style.display = "none"; // 隐藏容器
        }, 2000); // 2秒后隐藏提示消息
    }


    // 从文本文件中获取数据并创建滚动元素
    fetchDataFromFile("/static/datasets/scrolling_name.txt");

    scrollingText.addEventListener("mouseover", function() {
        this.style.animationPlayState = "paused";
    });

    scrollingText.addEventListener("mouseout", function() {
        this.style.animationPlayState = "running";
    });
});

