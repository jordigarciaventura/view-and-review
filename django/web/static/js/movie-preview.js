$(document).ready(() => {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $(".watchlist-option").click(e => {
        const target = $(e.currentTarget);

        const watchlist = target.data('watchlist');
        const url = target.data('url');

        $.ajax({
            type: (watchlist) ? 'DELETE' : 'POST',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: () => {
                target.data('watchlist', !watchlist);
                target.children().toggleClass('hidden');
            },
            error: xhr => {
                if (xhr.status == 401) {
                    redirectUrl = xhr.responseText
                    window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
                }
            }
        });
    });

    $(".favlist-option").click(e => {
        const target = $(e.currentTarget);

        const favorite = target.data('favlist');
        const url = target.data('url');

        $.ajax({
            type: (favorite) ? 'DELETE' : 'POST',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: () => {
                target.data('favlist', !favorite);
                target.children().toggleClass('hidden');
            },
            error: xhr => {
                if (xhr.status == 401) {
                    redirectUrl = xhr.responseText
                    window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
                }
            }
        });
    });

    $(".play-option").click(e => {
        const url = $(e.currentTarget).data('url');

        $.ajax({
            type: 'GET',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: data => {
                if (data == "None") {
                    alert("No trailer available")
                    return
                }

                key = data
                window.location.href = `https://www.youtube.com/embed/${key}?autoplay=1`
            }
        });

    });
});

