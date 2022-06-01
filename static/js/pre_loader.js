$(window).on("load",async function () {
    /*----- Preloader -----*/
    await new Promise(r => setTimeout(r, 1000));
    $(".preloader").fadeOut("slow");
    // $(".preloader").slideUp(1000).fadeOut("slow");
});
