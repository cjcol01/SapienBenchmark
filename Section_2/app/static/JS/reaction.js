let startTime;
let endTime;
let timeout;
let attempts = 0;
let totalReactionTime = 0;

// function to end test when when test complete
function endTest(averageReactionTime) {
    console.log("endTest called with averageReactionTime:", averageReactionTime);

    // getting elements
    const saveButton = document.getElementById("saveScore");
    const retryButton = document.getElementById("tryAgain");
    const reactionTimeDisplay = document.getElementById("reactionTime");
    const message = document.getElementById("name");
    const instructions = document.getElementById("instruction");

    // Show the final message and average reaction time
    message.textContent = "Reaction Time";
    reactionTimeDisplay.textContent = `${averageReactionTime.toFixed(0)} ms`;
    instructions.textContent = "Save your score and see how you compare";

    // Show the buttons
    saveButton.style.display = "inline-block";
    // retryButton.style.display = "inline-block";

    // Hide the test area's functionality by removing the click event listener
    const testArea = document.getElementById("reactionTestArea");
    testArea.onclick = null;
    testArea.classList.remove("green", "red", "blue");
    testArea.classList.add("blue");

    // Set the score in the hidden input field
    console.log(averageReactionTime.toFixed(0));
    document.getElementById("scoreInput").value = averageReactionTime.toFixed(0);

    // Automatically submit the form
    document.getElementById("scoreForm").submit();
}

// allows test to be restarted. removed from current version
function tryAgain() {
    // Reset the test
    attempts = 0;
    totalReactionTime = 0;
    document.getElementById("reactionTime").textContent = "";
    document.getElementById("saveScore").style.display = "none";
    document.getElementById("tryAgain").style.display = "none";
    document.getElementById("reactionTestArea").style.display = "block";
    document.getElementById("reactionTestArea").classList.add("blue");
}

// handle and time click events
function handleClick() {
    const testArea = document.getElementById("reactionTestArea");
    const message = document.getElementById("name");
    const dissapear = document.getElementById("instruction");
    const reactionTimeDisplay = document.getElementById("reactionTime");

    if (attempts >= 3) {
        // Dont allow more attempts if attempts
        return;
    }

    if (testArea.classList.contains("blue")) {
        testArea.classList.remove("blue");
        testArea.classList.add("red");
        message.textContent = "Wait for green";
        dissapear.textContent = "";

        const randomDelay = Math.random() * 2000 + 10; // Random time between 1 and 3 seconds
        timeout = setTimeout(() => {
            testArea.classList.replace("red", "green");
            if (attempts <= 2) {
                message.textContent = "Click!";
                startTime = new Date();
            }
        }, randomDelay);
    }
    // tests if user clicked appropriatly
    if (testArea.classList.contains("green")) {
        endTime = new Date();
        const reactionTime = endTime - startTime;
        totalReactionTime += reactionTime;
        attempts++;
        testArea.classList.remove("green");

        if (attempts >= 2) {
            const averageReactionTime = totalReactionTime / attempts;
            // Call endTest with the average reaction time
            endTest(averageReactionTime);
        } else {
            // If not, show the reaction time and reset for another try
            reactionTimeDisplay.textContent = `${reactionTime} ms. Try ${3 - attempts} more times!`;
            message.textContent = "Click to keep going";
            testArea.classList.add("blue");
        }
        clearTimeout(timeout);
    }
}

window.onload = () => {
    const testArea = document.getElementById("reactionTestArea");
    testArea.classList.add("blue");
};
