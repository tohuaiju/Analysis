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
    $("#search").keyup(function() {
        // 如果搜索框中有文字输入
        if($(this).val().length > 0) {
            // 添加前往图标的动画效果
            $(".go-icon").addClass("go-in");
        }
        else {
            // 移除前往图标的动画效果
            $(".go-icon").removeClass("go-in");
        }
    });

    $(".go-icon").click(function(){
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
    });

});


