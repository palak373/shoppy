$(document).ready(function(){

    /*
    * Progress Bar 
    */
    function progressBarInit(){
        let progress = $('#progressBar');
        let progressLine = progress.find('.indeterminate');
        progressLine.addClass('purple');
        progress.addClass('white');
        progress.css("margin", "0");
        progress.css("height", "2px")
        progress.css("display", "block");
    }
    function stopProgressBar(){
        let progress = $('#progressBar');
        let progressLine = progress.find('.indeterminate');
        progress.css("display", "none");
    }
    /*    
    * StripeModule JsRender
    */
    let stripeModule = $('.stripe-form');
    let stripeModuleToken = stripeModule.attr("data-publish-key");
    let stripeModuleNextUrl = stripeModule.attr("data-next-url");
    let stripeModuleBtnTitle = stripeModule.attr("data-btn-title");
    let stripeTemplate = $.templates("#stripeTemplate");
    let stripeTemplateData = {
        publish_key:stripeModuleToken,
        next_url:stripeModuleNextUrl,
        btn_title:stripeModuleBtnTitle
    }
    let stripeTemplateHtml = stripeTemplate.render(stripeTemplateData);
    stripeModule.html(stripeTemplateHtml);

    /*
    * STRIPE JS
    */
    let publish_key = $('#payment-form').attr('data-publish-key');
    let nextUrl = $('#payment-form').attr('data-next-url');        
    // Create a Stripe client.
    var stripe = Stripe(publish_key);

    // Create an instance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
        base: {
            color: '#32325d',
            lineHeight: '18px',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    // Handle form submission.
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        progressBarInit();
        stripe.createToken(card).then(function(result) {
            if (result.error) {
            // Inform the user if there was an error.
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
            // Send the token to your server.
                stripeTokenHandler(result.token, nextUrl);
            }
        });
    });

    function redirectToPath(nextUrl){
        if (nextUrl){
            setTimeout(function(){
                window.location.href = nextUrl;
            }, 1500);
        }
    }

    function stripeTokenHandler(token, nextUrl){
        let paymentEndpoint = '/billing/payment-method/create/'
        console.log(token);
        data= {
            "token": token.id
        }
        $.ajax({
            url: paymentEndpoint,
            method: "POST",
            data: data,
            success: function(data){
                //console.log(data);
                stopProgressBar();
                card.clear();

                $.alert({
                    title:"Success!",
                    type: 'purple',
                    content:data.message,
                    theme: 'material'
                });
                redirectToPath(nextUrl);
            },
            error: function(err){
                console.log(err);
            }
        });
    }
});
