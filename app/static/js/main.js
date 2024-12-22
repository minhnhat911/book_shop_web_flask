function addToCart(id, name, price) {
//    coi lai fetch de lm j
   fetch("/api/carts", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    }) // promise
}

function updateCart(productId, obj){
    fetch(`/api/cart/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        let quantities= document.getElementsByClassName("cart-counter");
        for(let quantity of quantities)
            quantity.innerText = data.total_quantity;

        let amount= document.getElementsByClassName("cart-amount");
        for(let item of amount)
            item.innerText = data.total_amount.toLocaleString("en-US");
    }) // promise
}

function pay(){
    fetch("/api/pay").then(res=>res.json()).then(data=>{
        if(data.status===200)
            location.reload();
        else
            alert("Có lỗi xảy ra!")
    })
}

function addToBill(obj){
 fetch("/api/create_bill", {
        method: "post",
        body: JSON.stringify({
            "id": obj.value
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsByClassName("bill-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    }) // promise
}
function updateBill(bookId,obj){
    fetch(`/api/create_bill/${bookId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        let bill_count= document.getElementsByClassName("bill-counter");
        for(let i of bill_count)
            i.innerText = data.total_quantity;

        let a= document.getElementsByClassName("bill-amount");
        for(let sum of a)
            sum.innerText = data.total_amount.toLocaleString("en-US");
    }) // promise
}
//
//}




