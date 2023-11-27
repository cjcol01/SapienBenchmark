word_list = [
    "apple",
    "tree",
    "cloud",
    "river",
    "mountain",
    "stone",
    "flower",
    "forest",
    "ocean",
    "sand",
    "bird",
    "sky",
    "star",
    "moon",
    "sun",
    "planet",
    "galaxy",
    "universe",
    "light",
    "dark",
    "fire",
    "water",
    "earth",
    "wind",
    "metal",
    "wood",
    "leaf",
    "rain",
    "snow",
    "storm",
    "thunder",
    "lightning",
    "wave",
    "peak",
    "valley",
    "island",
    "beach",
    "desert",
    "jungle",
    "volcano",
    "lake",
    "river",
    "stream",
    "pond",
    "glacier",
    "canyon",
    "cliff",
    "dune",
    "prairie",
    "hill",
    "field",
    "meadow",
    "marsh",
    "swamp",
    "bay",
    "gulf",
    "strait",
    "channel",
    "fjord",
    "sea",
    "ocean",
    "reef",
    "ridge",
    "plateau",
    "basin",
    "delta",
    "peninsula",
    "archipelago",
    "atoll",
    "cave",
    "grotto",
    "spring",
    "geyser",
    "waterfall",
    "rapids",
    "tundra",
    "savanna",
    "steppe",
    "forest",
    "rainforest",
    "taiga",
    "grassland",
    "wetland",
    "habitat",
    "ecosystem",
    "biosphere",
    "flora",
    "fauna",
    "species",
    "wildlife",
    "nature",
    "environment",
];

let seenWords = new Set();
let currentWord = "";
let score = 0;
let end_flag = 0;

function getRandomWord() {
    return word_list[Math.floor(Math.random() * word_list.length)];
}

function endGame() {
    // Set the score in the form and show the save button
    document.getElementById("verbalMemoryScoreInput").value = score;
    document.getElementById("saveVerbalMemory").style.display = "block";

    // Disable game buttons or other interactions
    document.getElementById("gameButton").style.display = "none";
}

function updateScore(correct) {
    const reactionTestArea = document.getElementById("reactionTestArea");

    if (correct) {
        score++;
    } else {
        // Flash #reactionTestArea red
        reactionTestArea.classList.add("flash-red");

        setTimeout(() => {
            reactionTestArea.classList.remove("flash-red");
        }, 500);

        end_flag++;
        if (end_flag >= 2) {
            endGame();
            return;
        }
        score = Math.max(0, score - 1); // remove point if incorrect, minimum score is 0
    }
    document.getElementById("scoreDisplay").innerText = "Score: " + score;
}

function displayWord() {
    currentWord = getRandomWord();
    document.getElementById("wordDisplay").innerText = currentWord;
}

function userResponse(seen) {
    let correct = false;

    if (seen && seenWords.has(currentWord)) {
        correct = true;
    } else if (!seen && !seenWords.has(currentWord)) {
        correct = true;
    }

    updateScore(correct);
    seenWords.add(currentWord);
    displayWord();
}

// Initial call to display the first word
window.onload = displayWord;
