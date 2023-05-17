document.addEventListener("DOMContentLoaded", () => { 

    document.querySelector(".search-option").addEventListener("click", () => {    
        document.querySelector(".search-close").style.display = "flex";
        document.querySelector(".navbar").classList.toggle("navbar-full");
        
        document.querySelector(".search-bar-container").style.display = "flex";
        document.querySelector(".search-bar-container").classList.toggle("search-bar-container-full");
    });

    document.querySelector(".search-close").addEventListener("click", () => {    
        document.querySelector(".search-close").style.display = "none";
        document.querySelector(".navbar").classList.toggle("navbar-full");
        
        document.querySelector(".search-bar-container").style.display = "";
        document.querySelector(".search-bar-container").classList.toggle("search-bar-container-full");
    
        document.querySelector(".search-input").value = "";
    });
});