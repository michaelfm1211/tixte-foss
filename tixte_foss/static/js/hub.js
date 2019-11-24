// Check For Dark Mode On Load
update_dark()

// Dark Mode

function toggle_dark() {
    if (localStorage.getItem("tixte_dark") === "false") {
        localStorage.setItem("tixte_dark", "true")
    } else if (localStorage.getItem("tixte_dark") === "true") {
        localStorage.setItem("tixte_dark", "false")
    } else if (localStorage.getItem("tixte_dark") === null) {
        localStorage.setItem("tixte_dark", "true")
    }

    update_dark()
}

function update_dark() {
    let playits = document.getElementsByClassName("gameicon");
    let soonits = document.getElementsByClassName("soonicon");

    if (localStorage.getItem("tixte_dark") === "false") {
        document.getElementById("template-sheet").href = "../static/third-party/sb-admin-2/sb-admin-2-light.css";

        for (let i = 0; i < playits.length; i++) {
            playits[i].src = "../static/img/playit/playit-light.svg";
        }
    }
    if (localStorage.getItem("tixte_dark") === "true") {
        document.getElementById("template-sheet").href = "../static/third-party/sb-admin-2/sb-admin-2-dark.css";
        for (let i = 0; i < playits.length; i++) {
            playits[i].src = "../static/img/playit/playit-dark.png";
        }
    }
    if (localStorage.getItem("tixte_dark") === null) {
        localStorage.setItem("tixte_dark", "false")
    }
}

// Search Box
$("#search-box-btn").on("click", function () {
    let value = $("#search-box").val().toLowerCase();
    let game = $("#games-container .game");
    game.hide()
    game.filter(function () {
        return $(this).find(".card .card-body .row .game-info .game-title").text().toLowerCase().indexOf(value) > -1
    }).show()
});