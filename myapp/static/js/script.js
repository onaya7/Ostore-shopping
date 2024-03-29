const header = document.querySelector("header");

window.addEventListener("scroll", function () {
    header.classList.toggle("sticky", window.scrollY > 0)
});

let menu = document.querySelector('#menu-icon');
let navlist = document.querySelector('.navlist');
let dropdown = document.querySelector('#dropdown')
let dropdownList = document.querySelector('.dropdown-list')

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navlist.classList.toggle('open');
}

dropdown.onclick = () => {
    dropdownList.classList.toggle('open')
}

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navlist.classList.remove('open');
}

const sr = ScrollReveal({
    distance: '30px',
    duration: 2600,
    reset: true
})

sr.reveal('.home-text', { delay: 280, origin: 'bottom' })

sr.reveal('.featured, .cta, .new, .brand, .contact', { delay: 200, origin: 'bottom' })


// Quantity wrapper
// const plus = document.querySelector(".plus"),
// minus = document.querySelector(".minus"),
// num = document.querySelector(".num");

// let a =1;

// plus.addEventListener("click", ()=>{
//     a++;
//     a = (a<10) ? "0" + a : a;
//     num.innerText = a;
//     console.log(a);
// });

// minus.addEventListener("click", ()=>{
//     if (a > 1){
//         a--;
//         a = (a<10) ? "0" + a : a;
//         num.innerText = a;
//     }
// });

// Quantity wrapper ends

// Toogle password visibility on auth
function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var confirm_passwordInput = document.getElementById("confirm_password");
    var toggleButton = document.getElementById("toggleButton");

    if (passwordInput.type && confirm_passwordInput.type === "password") {
        passwordInput.type = "text";
        confirm_passwordInput.type = "text";
        toggleButton.textContent = "Hide password";
    } else {
        passwordInput.type = "password";
        confirm_passwordInput.type = "password"
        toggleButton.textContent = "Reveal password";
    }
}

// $(document).ready(function () {
//     // Ajax for adding to cart
//     $('#add-to-cart-form').on('submit', function (event) {
//         $.ajax({
//             data: {
//                 quantity: $('#qty-num').val(),
//                 product_id:$('#product-id').val(),
//             },

//             type: 'POST',
//             url: '/addToCart'

//         })

//             .done(function (data) {
//                 console.log(data.message)

//                 // $('#message').text(data.message);

//             });
//         event.preventDefault();
//     });

// });