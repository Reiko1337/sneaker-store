// Скрытие уведомления

let close = document.getElementsByClassName('message__close')

for (let i = 0; i < close.length; i++) {
    close[i].addEventListener('click', function () {
        this.parentNode.remove()
    })
}



// Меню навигации

document.querySelector('.header__burger').addEventListener('click', function () {
    this.classList.toggle('active')
    document.getElementsByClassName('menu')[0].classList.toggle('active')
    document.body.classList.toggle('lock')
})

const spoiler = document.querySelectorAll('.footer__item-title')

for (let i = 0; i < spoiler.length; i++) {
    spoiler[i].addEventListener("click", function () {
        this.nextElementSibling.classList.toggle('spoiler-active')
    });
}



// Слайдео (index.html)

/* Индекс слайда по умолчанию */
let slideIndex = 1;
showSlides(slideIndex);

/* Функция увеличивает индекс на 1, показывает следующй слайд*/
function plusSlide() {
    showSlides(slideIndex += 1);
}

/* Функция уменьшяет индекс на 1, показывает предыдущий слайд*/
function minusSlide() {
    showSlides(slideIndex -= 1);
}

/* Устанавливает текущий слайд */
function currentSlide(n) {
    showSlides(slideIndex = n);
}

/* Основная функция слайдера */
function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("slider__item");
    let dots = document.getElementsByClassName("slider__dots-item");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}




// Slider <Вы недавно просматривали> 

let start = 0
showSneakersView()

document.addEventListener("DOMContentLoaded", function (event) {
    window.onresize = function () {
        showSneakersView()
    };
});

document.getElementById('prev-view').addEventListener('click', function () {

    let item_width = document.querySelector('.snekaer-group__col').offsetWidth
    let container_width = document.querySelector('.container').offsetWidth

    let count = Math.floor(container_width / item_width)

    start -= count
    showSneakersView();
})

document.getElementById('next-view').addEventListener('click', function () {
    let item_width = document.querySelector('.snekaer-group__col').offsetWidth
    let container_width = document.querySelector('.container').offsetWidth

    let count = Math.floor(container_width / item_width)

    start += count
    showSneakersView();
})

function showSneakersView() {
    let sneakers = document.querySelector('.view').children

    let item_width = document.querySelector('.snekaer-group__col').offsetWidth
    let container_width = document.querySelector('.container').offsetWidth

    let last = Math.floor(container_width / item_width) + start

    if (start <= 0) {
        document.getElementById('prev-view').setAttribute('disabled', true);
    }
    else {
        document.getElementById('prev-view').removeAttribute('disabled', false);
    }

    if (last >= sneakers.length) {
        document.getElementById('next-view').setAttribute('disabled', true);
    }
    else {
        document.getElementById('next-view').removeAttribute('disabled', false);
    }

    if (last > sneakers.length) {
        last = sneakers.length
        start = last - Math.floor(container_width / item_width)
    }
    if (start < 0) {
        start = 0
        last = Math.floor(container_width / item_width)
    }

    for (let i = 0; i < sneakers.length; i++) {
        if (i >= start && i <= last) {
            sneakers[i].style.display = 'block'
        }
        else {
            sneakers[i].style.display = 'none'
        }
    }
}