$(document).on('submit', '#review-form', e => {
    e.preventDefault();

    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    const elem = $(e.currentTarget);

    const title = $('#id_title').val();
    const content = $('#id_content').val();
    const url = $(e.currentTarget).attr('action');

    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        data: {
            title: title,
            content: content
        },
        success: data => {
            $('#rating-form').css('display', 'none');
            $('#review-form').css('display', 'none');
            $('#user-review-container').css('display', 'flex');
            $('#add-review').css('display', 'flex');
            $('.user-review').css('display', 'flex');
            
            $('.user-review').find('.title').val(title);
            $('.user-review').find('.body').val(content);
            $('.user-review').find('.user').text("You");

            $('.delete-rating').css('display', 'none');
            $('#edit-rating').css('display', 'flex');

            $('#info-bar .stars input').attr('disabled', true);
            
            $('.user-review .review').data('reviewId', data);
            $('.user-review .downvote').attr('active', false);
            $('.user-review .upvote').attr('active', false);
            $('.user-review .votes').text(0);

            $('#id_title').val("");
            $('#id_content').val("");
        },
        error: xhr => {
            if (xhr.status == 401) {
                redirectUrl = xhr.responseText
                window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
            }
        }
    });
});

$(document).ready( () => {
    $('#add-review').on('click', e => {
        const form = $('#review-form');
        form.css('display', 'flex');
        $(e.currentTarget).css('display', 'none');
    });

    $('#cancel-review').on('click', e => {
        const form = $('#review-form');
        form.css('display', 'none');
        $('#add-review').css('display', 'flex');
    });

    $('#show-more-cast').on('click', e => {
        $('#cast').toggleClass('show-all-rows');
        $(e.currentTarget).css('display', 'none');
    });

    $('#edit-rating').click(() => {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#user-review-container").offset().top
        }, 0, () => {
            $('.user-review .edit').click();
        });
    })
});