const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const message = document.querySelectorAll(".message");
const earth_left = document.querySelector(".left-panel-earth")
const earth_right = document.querySelector(".right-panel-earth")
let root = document.documentElement;

if (!container.classList.contains('sign-in-activate')) {
    root.style.setProperty('--earthMov', -500 + "px");
    earth_right.classList.add("hidden-main")
    earth_right.classList.remove("float")
    earth_left.classList.remove("hidden")
    earth_left.classList.add("float")
}

sign_up_btn.addEventListener("click", () => {
    if (message) {
        message.forEach((msg) => {
            msg.remove()
        })
    }

    console.log(1)
    root.style.setProperty('--earthMov', 500 + "px");
    container.classList.add("sign-in-activate");
    earth_right.classList.remove("hidden-main")
    earth_right.classList.remove("hidden")
    earth_right.classList.add("float")
    earth_left.classList.add("hidden")
    earth_left.classList.remove("float")


});


sign_in_btn.addEventListener("click", () => {
    if (message) {
        message.forEach((msg) => {
            msg.remove()
        })
    }
    root.style.setProperty('--earthMov', -500 + "px");
    container.classList.remove("sign-in-activate");
    earth_right.classList.add("hidden")
    earth_right.classList.remove("float")
    earth_left.classList.remove("hidden")
    earth_left.classList.add("float")

});
