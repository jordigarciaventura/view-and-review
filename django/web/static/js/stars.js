$(document).ready(() => {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    
    $('.user-rating input').click(e => {
        const target = $(e.currentTarget);
        
        const value = target.val();
        const url = target.closest('.stars').data('url');

        $.ajax({
            type: 'POST',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                'rating': value
            },
            success: data => {
                updateScore(data.value, data.count);
                updateStars(value);
                showDeleteRating();
                if ($('#review-form').is(":hidden"))
                    $('#add-review').css('display', 'flex');
            },
            error: xhr => {
                target.prop('checked', false);
                
                if (xhr.status == 401) {
                    redirectUrl = xhr.responseText
                    window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
                }
            }
        });
    });

    $('.delete-rating').click(e => {
        const target = $(e.currentTarget);
        
        const url = target.siblings('.stars').data('url');

        $.ajax({
            type: 'DELETE',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: data => {
                updateScore(data.value, data.count);
                updateStars(0);
                hideDeleteRating();
                $('#add-review').css('display', 'none');
                $('#review-form').css('display', 'none');
                $('#user-review-container').css('display', 'none');

                $('#info-bar .stars input').attr('disabled', false);
            },
            error: xhr => {
                if (xhr.status == 401) {
                    redirectUrl = xhr.responseText
                    window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
                }
            }
        });
    });
});


function updateScore(score, count) {
    const backgroundStyle = `radial-gradient(closest-side, #222222 79%, transparent 80% 100%),conic-gradient(hsl(calc(${score} * 1.2), 100%, 50%) ${score}%, #606060 0)`;

    const scoreDiv = $('#score');

    scoreDiv.find('.score-text').html(score ? score : '-');
    scoreDiv.find('.score-amount').html(count);
    
    const circle = scoreDiv.find('.progress-circle');
    circle.attr('aria-valuenow', score);
    circle.css('background', backgroundStyle);
}

function updateStars(score) {
    $('.user-rating input').prop('checked', function() {
        return $(this).val() == score;
    });
}

function hideDeleteRating() {
    $('.delete-rating').css('display', 'none');
}

function showDeleteRating() {
    if ($('#edit-rating').is(":hidden"))
        $('.delete-rating').css('display', 'flex');
}