const favorite_checkbox = document.querySelectorAll('.sneaker-group__item-favorite-checkbox')
const xhr = new XMLHttpRequest()

for (let i = 0; i < favorite_checkbox.length; i++) {
    favorite_checkbox[i].addEventListener("click", function () {

        const url = this.parentElement.action + '?'
        xhr.open('GET', url + 'favorite=' + this.checked)
        // xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

        xhr.onreadystatechange = function(){
            if(xhr.readyState == 4 && xhr.status == 200){
//                let data = JSON.parse(xhr.response);
            }
        }

        xhr.send()
    })
}