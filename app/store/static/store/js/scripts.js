// document.querySelector('input[type="submit"]').addEventListener('click', function (e) {
//     e.preventDefault();
//     let form = document.getElementById('sneaker-cart__form')
//     let checkboxs = [...document.querySelectorAll('#sneaker-cart__form-label>input[type="checkbox"]')]
//     for(i=0; i<checkboxs.length;i++){
//         if (checkboxs[i].checked == true) {
//             console.log('checkbox checked'); 
//             form.submit()
//             return
//         }
//     }   
//     let message = `<section class="message">'
//     <div class="container">
//         <div class="message__inner">
//             <div class="message__item info">
//                 <p class="message__text">Вы не выбрали размер кроссовк</p>
//                 <button class="message__close" type="button">&times;</button>
//             </div>
//         </div>
//     </div>
// </section>`
//     let header = document.getElementsByClassName('header')[0].insertAdjacentHTML('afterEnd', message)
// });


let close = document.getElementsByClassName('message__close')

for (let i = 0; i < close.length; i++){
    close[i].addEventListener('click', function(){
        this.parentNode.remove()
    })
}