$(document).ready(() => {
    $(".search-option").click(() => {    
        $(".search-close").css("display", "flex");
        $(".navbar").toggleClass("navbar-full");
        
        $(".search-bar-container").css("display", "flex");
        $(".search-bar-container").toggleClass("search-bar-container-full");
    });

    $(".search-close").click( () => {    
        $(".search-close").css("display", "none");
        $(".navbar").toggleClass("navbar-full");
        
        $(".search-bar-container").css("display", "");
        $(".search-bar-container").toggleClass("search-bar-container-full");

        $(".search-input").value = "";
    });
});