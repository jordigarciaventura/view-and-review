document.addEventListener("DOMContentLoaded", () => { 
    let searching = false;
    
    let searchOptionElem = document.querySelector(".search-option");
    let searchCloseElem = document.querySelector(".search-close");

    searchOptionElem.addEventListener("click", () => {
        document.querySelector(".logo").style.display = "none";
        document.querySelector(".nav-options").style.display = "none";
        document.querySelector(".search-bar").style.display = "flex";
        document.querySelector(".search-close").style.display = "flex";
        document.querySelector(".search-close").style.display = "flex";
        document.querySelector(".navbar").classList.toggle("navbar-full");
        document.querySelector(".search-bar").classList.toggle("search-bar-full");

        searching = true;
    });

    searchCloseElem.addEventListener("click", () => {
        document.querySelector(".search-input").value = "";
        document.querySelector(".search-close").style.display = "none";
    
        document.querySelector(".logo").style.display = "flex";
        document.querySelector(".nav-options").style.display = "flex";
        document.querySelector(".search-bar").style.display = "none";
        document.querySelector(".search-close").style.display = "none";
        document.querySelector(".navbar").classList.toggle("navbar-full");
        document.querySelector(".search-bar").classList.toggle("search-bar-full");
    });
});