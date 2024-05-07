const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
let visContainer = document.getElementById('vis2'); // 更改为 let，以便后续更新

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");

    if (visContainer) {
        visContainer.parentNode.removeChild(visContainer);
        visContainer = null; // 移除后将 visContainer 设为 null
    }
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
    visContainer = document.getElementById('vis2'); // 重新获取 vis2 元素
    if (!visContainer) {
        // 创建 vis2 元素
        const vis = document.createElement('div');
        vis.id = 'vis2';
        container.appendChild(vis);
        visContainer = vis; // 更新 visContainer
    }
});

