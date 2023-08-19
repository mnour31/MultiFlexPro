var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0 ; i < updateBtns.length ; i++) {
    updateBtns[i].addEventListener('click' , function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('product:' , productId , 'action:' , action )

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            console.log('this user not loging')
        }else{
            updateUserOrder(productId , action)
        }
    }) 
}

function updateUserOrder(productId , action){
    console.log('this user is login and sending data')


    let url = shopName

    fetch(
        url,{
            method:'POST',
            headers:{
                'Content-Type':'application/Json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'productId':productId , 'action':action})
        })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            location.reload()
        })
}


