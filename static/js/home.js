$(document).ready(function () {

    // Navbar Shrink
    $(window).on("scroll",function(){
        if($(this).scrollTop() > 70){
            $(".navbar").addClass("navbar-shrink");
            $(".navbar-brand").removeClass("d-lg-none");
        }
        else{
            $(".navbar").removeClass("navbar-shrink");
            $(".navbar-brand").addClass("d-lg-none");
        }
    });

     // Carousel
     $('.testimonials-carousel').owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            1000:{
                items:3,
            }
        }
    })

    // Page Scroll
    $.scrollIt({
        topOffset: -50
    });

     // Navbar Collapse
     $(".nav-link").on("click", function(){
         $(".navbar-collapse").collapse("hide");
     });

});
