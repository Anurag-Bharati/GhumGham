$(window).on("load",async function () {
    /*----- Preloader -----*/
    await new Promise(r => setTimeout(r, 500));
    $(".preloader").fadeOut("fast");
    // $(".preloader").slideUp(1000).fadeOut("slow");
});
