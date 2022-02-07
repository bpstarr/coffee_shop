function getPrice(size_name,product_id) {
    var jsonObject = {
        'size_name':size_name,
        'product_id':product_id
        };
    var quantity = document.getElementById(`quantity-${product_id}`).value;
    $.ajax({
        url:'/show_price',
        data: JSON.stringify(jsonObject),
        type:'POST',
        success:function(response) {
            var test = JSON.parse(response);
            if (quantity == 1) {
            $(`#print_price-${test.product_id}`).html('Price: '+ '$' + test.price);
            }
            else if (quantity > 1){
                $(`#print_price-${test.product_id}`).html('Price: '+ '$' + ((test.price)*quantity).toFixed(2));
            }
        },
        error:function(response) {
            $(`#print_price-${product_id}`).html('Price: ');
        },
        datatype:'json',
        contentType:'application/json; charset=utf-8'
        
    });
}

function updatePrice(quantity,product_id,size_name) {
    jsonObject = {
        'quantity': quantity,
        'product_id': product_id,
        'size_name': size_name
    }
    
    $.ajax({
        url:'/show_price',
        data: JSON.stringify(jsonObject),
        type:'POST',
        success:function(response) {
            var test = JSON.parse(response);
            if (quantity == 1) {
            $(`#print_price-${test.product_id}`).html('Price: '+ '$' + test.price);
            }
            else if (quantity > 1){
                $(`#print_price-${test.product_id}`).html('Price: '+ '$' + ((test.price)*quantity).toFixed(2));
            }
    },
    error:function(response) {
        $(`#print_price-${product_id}`).html('Price: ');
    },
    datatype:'json',
    contentType:'application/json; charset=utf-8'
})
}

function getPriceEdit(size_name,product_id){
    jsonObject = {
        'product_id': product_id,
        'size_name': size_name
    }
    $.ajax({
        url:'/show_price',
        data: JSON.stringify(jsonObject),
        type:'POST',
        success:function(response) {
            var test = JSON.parse(response);
            $(`#print_price-${test.product_id}`).val(test.price);
            
    },
    error:function(response) {
        $(`#print_price-${product_id}`).val('Price');
    },
    datatype:'json',
    contentType:'application/json; charset=utf-8'
})
}

var time = new Date().getTime();
    $(document.body).bind("mousemove keypress", function(e) {
        time = new Date().getTime();
    });

    function refresh() {
        if(new Date().getTime() - time >= 15000) 
            window.location.reload(true);
        else 
            setTimeout(refresh, 10000);
    }

    setTimeout(refresh, 10000);












