const header = document.querySelector("header");

window.addEventListener ("scroll",  function(){
    header.classList.toggle("sticky",  window.scrollY > 0)
});

let menu = document.querySelector('#menu-icon');
let navlist = document.querySelector('.navlist');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navlist.classList.toggle('open');
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

sr.reveal('.home-text', {delay:280, origin:'bottom'}) 

sr.reveal('.featured, .cta, .new, .brand, .contact', {delay:200, origin:'bottom'})





// Quantity wrapper
const plus = document.querySelector(".plus"),
minus = document.querySelector(".minus"),
num = document.querySelector(".num");

let a =1;

plus.addEventListener("click", ()=>{
    a++;
    a = (a<10) ? "0" + a : a;
    num.innerText = a;
    console.log(a);
});

minus.addEventListener("click", ()=>{
    if (a > 1){
        a--;
        a = (a<10) ? "0" + a : a;
        num.innerText = a;
    }
});

// Quantity wrapper ends


