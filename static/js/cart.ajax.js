$(document).ready(function (){
    /**
     * Product ADD_REMOVE AJAX SHORTCUT
     */

    $(document).ready(function(){

        let addRemoveShortcut = $('.add-remove-shortcut-btn');
        addRemoveShortcut.click(function(e){
            let self = $(this);
            let actionUrl = self.attr("data-action");
            let method = self.attr("data-method");
            let productId = self.attr("data-product-id");
            let csrfToken = self.attr("data-csrf");
            let data = {
                "product_id":productId,
                "csrftoken": csrfToken
            }

            $.ajax({
                url:actionUrl,
                method: method,
                data: data,

                success: function(data){
                    console.log(data);
                    $('.cart-item-count').text(data.cartItemCount);
                    if(data.added){
                        self.html('<i class="material-icons add-remove-icon">remove</i>');
                        Materialize.toast('Item Added to Cart', 3000, 'rounded');
                    }else{
                        self.html('<i class="material-icons add-remove-icon">add</i>');
                        Materialize.toast('Item Removed from Cart', 3000, 'rounded');                        
                    }
                },
                error: function(err){
                    console.log(err);
                    $.alert({
                        title:"Oops!",
                        content:err.responseJSON.message,
                        theme: 'dark'
                    });
                }
            });
        });
    });

    /**
     * Product ADD_REMOVE AJAX
     */
    let productAddRemoveForm = $('.product-add-remove-form');
    productAddRemoveForm.submit(function(e){
        let self = $(this);
        let actionUrl = self.attr("action");
        let method = self.attr("method");
        let data = self.serialize();
        console.log(data);

        $.ajax({
            url:actionUrl,
            method:method,
            data: data,

            success: function(data){
                if(data.added){
                    $('.submit-btn').html(`<button type="submit" class="btn yellow black-text col s12">Remove</button>`);
                    Materialize.toast('Item Added to Cart', 3000, 'rounded');                    
                }else {
                    $('.submit-btn').html(`<button type="submit" class="btn yellow black-text col s12">Add To Cart</button>`);
                    Materialize.toast('Item Removed from Cart', 3000, 'rounded');                    
                }
                $('.cart-item-count').text(data.cartItemCount);
                if(window.location.href.indexOf("cart") != -1){
                    updateCart();
                }
            },

            error : function(err){
                $.alert({
                    title:"Oops!",
                    content: err.responseJSON.message,
                    theme: 'dark'
                });
            }
        })
        e.preventDefault();
    });
    function updateCart(){
        let cartTable = $('.cart-table');
        let cartTableBody = cartTable.find('.cart-table-body');
        let productRow = cartTableBody.find('.cart-products');
        let currentUrl = window.location.href
        let actionUrl = '/api/cart/';
        let method = "GET";
        let data = {};

        $.ajax({
            url: actionUrl,
            method: method,
            data: data,

            success: function(data){
                let hiddenRemoveForm = $('.hidden-remove-form');
                if (data.products.length > 0){
                    $('.cart-product').html(" ");
                    $.each(data.products, function(i, val){
                        let newCartItemRemoveForm = hiddenRemoveForm.clone();
                        newCartItemRemoveForm.css("display", "block");
                        newCartItemRemoveForm.find('.cart-item-product-id').val(val.id);
                        cartTableBody.prepend(`
                            <tr class="cart-product">
                                <td>${val.title}</td>
                                <td>hmmmm</td>
                                <td>${val.price}</td>
                                <td>${newCartItemRemoveForm.html()}</td>
                            </tr>
                        `);
                    });
                    
                    $('.cart-subtotal').text(data.subtotal);
                    $('.cart-total').text(data.total);
                }else{
                    window.location.href = currentUrl;
                }
            },
            error: function(err){
                $.alert({
                    title:"Oops!",
                    content: err.responseJSON.message,
                    theme: 'dark'
                });
            }
        })
    }
    

});