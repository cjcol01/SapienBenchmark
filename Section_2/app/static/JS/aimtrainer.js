let totalTimeToClick = 0;
let clickCount = 0;

document.addEventListener("DOMContentLoaded", () => {
    const target = document.querySelector('[data-aim-target="true"]');
    const clickCountDisplay = document.getElementById("clickCount");
    const timeToClickDisplay = document.getElementById("timeToClick");
    const gameArea = document.querySelector(".box");
    const saveScoreButton = document.getElementById("saveScore");
    let lastClickTime = Date.now();
    const MAX_CLICKS = 3;

    target.addEventListener("click", () => {
        clickCount++;
        const currentTime = Date.now();
        const timeTaken = currentTime - lastClickTime;
        totalTimeToClick += timeTaken; // Add the time taken for this click to the total

        clickCountDisplay.textContent = clickCount;
        timeToClickDisplay.textContent = timeTaken;
        lastClickTime = currentTime;

        if (clickCount < MAX_CLICKS) {
            moveTargetRandomly();
        } else {
            saveScoreButton.style.display = "block";
            target.style.display = "none";
        }
    });

    function moveTargetRandomly() {
        const maxLeft = gameArea.clientWidth - target.offsetWidth;
        const maxTop = gameArea.clientHeight - target.offsetHeight;

        const randomLeft = Math.floor(Math.random() * maxLeft);
        const randomTop = Math.floor(Math.random() * maxTop);

        target.style.left = randomLeft + "px";
        target.style.top = randomTop + "px";
    }
});

function calculateFinalScore() {
    console.log("Total Time to Click:", totalTimeToClick);
    console.log("Click Count:", clickCount);

    if (clickCount > 0) {
        const averageTimePerClick = totalTimeToClick / clickCount;
        console.log("Average Time Per Click:", averageTimePerClick);
        return Math.round(averageTimePerClick);
    } else {
        return 0; // Default score if no clicks were made
    }
}
function endAimTest() {
    const score = calculateFinalScore();
    document.getElementById("scoreInput").value = score;

    // Submit the form
    document.getElementById("scoreForm").submit();
}
function saveScore() {
    endAimTest();
}
