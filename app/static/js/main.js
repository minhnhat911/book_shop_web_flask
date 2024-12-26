function updateUI(data){
  let items = document.getElementsByClassName("cart-counter");
    for (let item of items)
        item.innerText = data.total_quantity;

    let amounts = document.getElementsByClassName("cart-amount");
    for (let item of amounts)
        item.innerText = data.total_amount.toLocaleString();
}


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

function updateCart(bookId, obj){
    fetch(`/api/cart/${bookId}`, {
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

function deleteCart(bookId) {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
         fetch(`/api/carts/${bookId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            updateUI(data);
            document.getElementById(`cart${bookId}`).style.display = "none";
        });
    }
}

function order(){
    fetch("/api/order").then(res=>res.json()).then(data=>{
        if(data.status===200){
            alert('Đặt sách thành công mã hóa đơn là: '+data.id)
            location.reload();}
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
        let quantities= document.getElementsByClassName("bill-counter");
        for(let quantity of quantities)
            quantity.innerText = data.total_quantity;

        let amount= document.getElementsByClassName("bill-amount");
        for(let item of amount)
            item.innerText = data.total_amount.toLocaleString("en-US");
    }) // promise
}
//
//}

function addComment(bookId) {
    fetch(`/api/book/${bookId}/comments`, {
        method: "post",
        body: JSON.stringify({
            "content": document.getElementById("comment").value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(c => {
        let html = `
        <li class="list-group-item">

            <div class="row">
                <div class="col-md-1 col-4">
                    <img src="${ c.user.avatar }" class="img-fluid rounded-circle" />
                </div>
                <div class="col-md-11 col-8">
                    <p>${ c.content }</p>
                    <p class="date">${ moment(c.created_date).locale("vi").fromNow() }</p>
                </div>
            </div>

        </li>
        `;

        let comments = document.getElementById("comments");
        comments.innerHTML = html + comments.innerHTML;
    })
}

function pay_bill(billId){
   fetch("/api/pay_bill", {
        method: "post",
        body: JSON.stringify({
            "id": billId
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        if(data.status===200)
            location.reload();
        else
            alert("Có lỗi xảy ra!")
    }) // promise
}




