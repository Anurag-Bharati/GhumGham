$(document).ready(function () {

    // Navbar Shrink
    $(window).on("scroll", function () {
        if ($(this).scrollTop() > 70) {
            $(".navbar").addClass("navbar-shrink");
            $(".navbar-brand").removeClass("d-lg-none");
        } else {
            $(".navbar").removeClass("navbar-shrink");
            $(".navbar-brand").addClass("d-lg-none");
        }
    });

    // Page Scroll
    $.scrollIt({
        topOffset: -50
    });

    // Navbar Collapse
    $(".nav-link").on("click", function () {
        $(".navbar-collapse").collapse("hide");
    });
    let book = $(".booking-card");
    let hitBox = $("#hit-box");

    $('#book-now').on("click", function () {
        $('html').css({'scroll-behavior': 'unset'})
        window.scrollTo(0, 0);
        $('body').css({'overflow': 'hidden'});
        $(document).bind('scroll', function () {
            window.scrollTo(0, 0);
        });
        book.removeClass("hide-booking");
        $(".booking-card ~ section > .container").animate({opacity: '0'});
    });
    hitBox.on("click", function () {
       $(".booking-card ~ section > .container").animate({opacity: '1'});
        $('html').css({'scroll-behavior': 'smooth'})

        $(document).unbind('scroll');
        $('body').css({'overflow': 'visible'});
        book.addClass("hide-booking");

    });

});


