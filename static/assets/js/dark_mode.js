
     // Toggle Theme
     function toggleTheme(){
         if(localStorage.getItem("active-theme") !== null){
            if(localStorage.getItem("active-theme") === "dark"){
                $("body").addClass("dark");
            }
            else{
                $("body").removeClass("dark");
            }
         }
        updateIcon();
    }
    toggleTheme();

    $(".toggle-theme").on("click", function(){
       $("body").toggleClass("dark");
       if($("body").hasClass("dark")){
           localStorage.setItem("active-theme","dark")
       }
       else{
           localStorage.setItem("active-theme","light")
       }
       updateIcon();
    });

    function updateIcon() {
        if ($("body").hasClass("dark")) {
            $(".toggle-theme i").removeClass("fa-moon");
            $(".toggle-theme i").addClass("fa-sun");
        } else {

            $(".toggle-theme i").removeClass("fa-sun");
            $(".toggle-theme i").addClass("fa-moon");
        }
    }

