function generateDeviceHash() {
    const data =
        navigator.userAgent +
        screen.width +
        screen.height +
        Intl.DateTimeFormat().resolvedOptions().timeZone;

    return btoa(data);
}

const loginBtn = document.getElementById("loginBtn");
const voteSection = document.getElementById("voteSection");
const submitVoteBtn = document.getElementById("submitVoteBtn");

let deviceHash = "";

// STEP 1: LOGIN
loginBtn.addEventListener("click", () => {
    deviceHash = generateDeviceHash();

    loginBtn.style.display = "none";
    voteSection.style.display = "block";
});

// STEP 2: SUBMIT VOTE
submitVoteBtn.addEventListener("click", () => {
    const selected = document.querySelector('input[name="vote"]:checked');

    if (!selected) {
        alert("Please select a candidate");
        return;
    }

    fetch("http://127.0.0.1:5000/vote", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            choice: selected.value,
            device_hash: deviceHash
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    })
    .catch(() => {
        alert("Backend not reachable");
    });
});
