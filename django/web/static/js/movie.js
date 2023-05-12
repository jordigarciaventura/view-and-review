$(document).ready(() => {
    $(".watchlist-option").click(e => {
        const movieID = $(e.currentTarget).data('movie-id');
        
        const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: 'POST',
            url:`/watchlist/${movieID}`,
            beforeSend: function (xhr){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            statusCode: {
                401: () => { 
                    window.location.href = `/accounts/login/?next=${window.location.pathname}`;
                }
            },
            success: data => {
                console.log("success");
                $(e.currentTarget).children().toggleClass('hidden');
            }
        });
    });

    $(".favorite-option").click(e => {
        const movieID = $(e.currentTarget).data('movie-id');
        
        const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: 'POST',
            url:`/favorite/${movieID}`,
            beforeSend: function (xhr){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            statusCode: {
                401: () => { 
                    window.location.href = `/accounts/login/?next=${window.location.pathname}`;
                }
            },
            success: data => {
                console.log("success");
                $(e.currentTarget).children().toggleClass('hidden');
            }
        });
    });

    $(".play-option").click(e => {
        const movieID = $(e.currentTarget).data('movie-id');

        const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: 'GET',
            url:`/trailer/${movieID}`,
            beforeSend: function (xhr){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: data => {
                console.log(data);
            }
        });

    });
});

