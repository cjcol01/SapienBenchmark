document.addEventListener('DOMContentLoaded', () => {
    const target = document.querySelector('[data-aim-target="true"]');
    const clickCountDisplay = document.getElementById('clickCount');
    const timeToClickDisplay = document.getElementById('timeToClick');
    const gameArea = document.querySelector('.box'); // Reference the .box element
    let clickCount = 0;
    let lastClickTime = Date.now();

    target.addEventListener('click', () => {
        clickCount++;
        clickCountDisplay.textContent = clickCount;

        const currentTime = Date.now();
        const timeTaken = currentTime - lastClickTime;
        timeToClickDisplay.textContent = timeTaken;
        lastClickTime = currentTime;

        moveTargetRandomly();
    });

    function moveTargetRandomly() {
        const maxLeft = gameArea.clientWidth - target.offsetWidth;
        const maxTop = gameArea.clientHeight - target.offsetHeight;

        const randomLeft = Math.floor(Math.random() * maxLeft);
        const randomTop = Math.floor(Math.random() * maxTop);

        target.style.left = randomLeft + 'px';
        target.style.top = randomTop + 'px';
    }
});
