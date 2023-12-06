let totalTimeToClick = 0;
let clickCount = 0;

// event listner to play on page load
document.addEventListener("DOMContentLoaded", () => {
    // getting elements
    const target = document.querySelector('[data-aim-target="true"]');
    const clickCountDisplay = document.getElementById("clickCount");
    const timeToClickDisplay = document.getElementById("timeToClick");
    const gameArea = document.querySelector(".box");
    const saveScoreButton = document.getElementById("saveScore");
    let lastClickTime = Date.now();
    const MAX_CLICKS = 5;

    // listening for user click
    target.addEventListener("click", () => {
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

    // moves targets to random location when user clicks
    function moveTargetRandomly() {
        const maxLeft = gameArea.clientWidth - target.offsetWidth;
        const maxTop = gameArea.clientHeight - target.offsetHeight;

        const randomLeft = Math.floor(Math.random() * maxLeft);
        const randomTop = Math.floor(Math.random() * maxTop);

        target.style.left = randomLeft + "px";
        target.style.top = randomTop + "px";
    }
});

// calculates score based on average time taken to clikc
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

// ends the test when all targets have been clicked on
function endAimTest() {
    const score = calculateFinalScore();
    document.getElementById("scoreInput").value = score;

    // Display the game over popup
    const gameOverPopup = document.getElementById("gameOverPopup");
    document.getElementById("averageTimeMessage").textContent = score + " MS";
    gameOverPopup.style.display = "block";
    console.log("Game Over");
}

// calls save score when button is clicked
function saveScore() {
    document.getElementById("scoreForm").submit();
    // endAimTest();
}
