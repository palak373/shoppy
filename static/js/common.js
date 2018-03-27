$(document).ready(function(){
    $(".button-collapse").sideNav();
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true,
    });        
    
    $('.slider').slider();
    $('.materialboxed').materialbox();



    /****** CONTACT_FORM *******/

    let contactForm = $('.contact-form');
    contactForm.submit(function(e){
        let self = $(this);
        let actionUrl = self.attr("action");
        let method = self.attr("method");
        let data = self.serialize();

        $.ajax({
            url: actionUrl,
            method: method,
            data: data,

            success: function(data){
                $.alert({
                    title:"Thanks",
                    content: data.message,
                    theme: 'dark'
                });
            },
            error: function(err){
                $.alert({
                    title:"Oops!",
                    content: err.responseJSON.message,
                    theme: 'dark'
                });
            }

        });
    });

});

