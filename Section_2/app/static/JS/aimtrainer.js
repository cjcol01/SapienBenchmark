let totalTimeToClick = 0;
let clickCount = 0;

document.addEventListener("DOMContentLoaded", () => {
    const target = document.querySelector('[data-aim-target="true"]');
    const clickCountDisplay = document.getElementById("clickCount");
    const timeToClickDisplay = document.getElementById("timeToClick");
    const gameArea = document.querySelector(".box");
    const saveScoreButton = document.getElementById("saveScore");
    const preGameTextTop = document.getElementById("preGameTextTop");
    const preGameTextBottom = document.getElementById("preGameTextBottom");

    let lastClickTime = Date.now();
    const MAX_CLICKS = 5;

    target.addEventListener("click", () => {
        if (clickCount === 0) {
            // This means the game is just starting
            preGameTextTop.style.display = "none";
            preGameTextBottom.style.display = "none";
            target.style.backgroundColor = "red"; // Change target background to red
        }
        clickCount++;
        const currentTime = Date.now();
        const timeTaken = currentTime - lastClickTime;
        totalTimeToClick += timeTaken; // Add the time taken for this click to the total

        // clickCountDisplay.textContent = clickCount;
        // timeToClickDisplay.textContent = timeTaken;
        lastClickTime = currentTime;

        if (clickCount < MAX_CLICKS) {
            moveTargetRandomly();
        } else {
            endAimTest();
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

    // Display the game over popup
    const gameOverPopup = document.getElementById("gameOverPopup");
    document.getElementById("averageTimeMessage").textContent = score + " MS";
    gameOverPopup.style.display = "block";
    console.log("Game Over");
}
function saveScore() {
    document.getElementById("scoreForm").submit();
    // endAimTest();
}
