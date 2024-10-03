window.addEventListener("load", setup);

function setup() {
    get_DOM_References();
}

function handle_clicked(input) {
    order_summary.value += input + "\n";
    console.log(input);
}

function get_DOM_References() {
    order_summary = document.getElementById("order_summary");
}
