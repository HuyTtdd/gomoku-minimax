let size = 20
let board = document.getElementById("board");

(function () {

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            let square = document.createElement("div");
            square.classList.add("square", i + "-" + j);

            square.style.top = 40 * i + "px";
            square.style.left = 40 * j + "px";

            board.appendChild(square);
        }
    }
}());

let clear_board = function () {
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            $(".square." + i + "-" + j).text("");
        }
    }
};