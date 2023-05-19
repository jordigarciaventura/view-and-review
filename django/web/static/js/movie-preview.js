$(document).ready(() => {
    const urls = JSON.parse(document.getElementById('urls').textContent);
    console.log(urls);

    $(".watchlist-option").click(e => {
        const target = $(e.currentTarget);
        const movieID = target.data('movie-id');
        const watchlist = target.data('watchlist');

        const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type:  (watchlist) ? 'DELETE' : 'POST',
            url: urls['watchlist'],
            beforeSend: function (xhr){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                'movie_id': movieID
            },
            statusCode: {
                401: () => { 
                    window.location.href = `${urls['login']}/?next=${window.location.pathname}`;
                }
            },
            success: data => {
                console.log("success");
                target.data('watchlist', !watchlist);
                target.children().toggleClass('hidden');
            }
        });
    });

    $(".favlist-option").click(e => {
        const target = $(e.currentTarget);
        const movieID = target.data('movie-id');
        const favorite = target.data('favlist');

        const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: (favorite) ? 'DELETE' : 'POST',
            url: urls['favlist'],
            beforeSend: function (xhr){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                'movie_id': movieID
            },
            statusCode: {
                401: () => { 
                    window.location.href = `${urls['login']}/?next=${window.location.pathname}`;
                }
            },
            success: data => {
                target.data('favlist', !favorite);
                console.log("success");
                target.children().toggleClass('hidden');
            }
        });
    });

    $(".play-option").click(e => {
        const movieID = $(e.currentTarget).data('movie-id');

        const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: 'GET',
            url: urls['trailer'],
            beforeSend: function (xhr){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                'movie_id': movieID
            },
            success: data => {
                if(data == "None") {   
                    alert("No trailer available")
                    return
                }

                key = data
                url = `https://www.youtube.com/embed/${key}?autoplay=1`
                window.location.href = url
            }
        });

    });
});

