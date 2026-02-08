const sidebar = document.getElementById("sidebar");
const bottomPanel = document.getElementById("bottom-panel");

document.getElementById("toggle-sidebar").onclick = () => {
    sidebar.classList.toggle("closed");
};

document.getElementById("toggle-bottom").onclick = () => {
    bottomPanel.classList.toggle("closed");
};
