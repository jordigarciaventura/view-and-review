$(document).ready(() => {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $('.user-review .delete').click(function() {
        const url = $(this).closest('.user-review').data('reviewUrl');

        $.ajax({
            type: 'DELETE',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: data => {
                $(this).closest('.user-review').css('display', 'none');
                $('#rating-form').css('display', 'flex');

                $('#edit-rating').css('display', 'none');
                $('.delete-rating').css('display', 'flex');
                
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

    $('.user-review .save').click(function() {
        const url = $(this).closest('.user-review').data('reviewUrl');

        const title = $(this).closest('.review-box').find('.title').val();
        const body = $(this).closest('.review-box').find('.body').val();

        $.ajax({
            type: 'PUT',
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                title: title,
                content: body
            },
            success: data => {                
                $(this).siblings('.cancel').css('display', 'none');
                $(this).css('display', 'none');
                $(this).siblings('.edit').css('display', 'flex');
                $(this).siblings('.delete').css('display', 'flex');

                $(this).closest('.review-box').find('.title').attr('readonly', true);
                $(this).closest('.review-box').find('.body').attr('readonly', true);
                $(this).closest('.review-box').find('input[type=radio]').attr('disabled', true);
            },
            error: xhr => {
                if (xhr.status == 401) {
                    redirectUrl = xhr.responseText
                    window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
                }
            }
        });
    });  

    let prevTitle = '';
    let prevBody = '';
    let prevScore = 0;

    $('.user-review .edit').click(function() {
        prevTitle = $(this).closest('.review-box').find('.title').val();
        prevBody = $(this).closest('.review-box').find('.body').val();
        prevScore = $(this).closest('.review-box').find('input[type="radio"]:checked').val();

        $(this).closest('.review-box').find('.title').attr('readonly', false);
        $(this).closest('.review-box').find('.body').attr('readonly', false);
        $(this).siblings('.save').css('display', 'flex');
        $(this).siblings('.cancel').css('display', 'flex');

        $(this).siblings('.delete').css('display', 'none');
        $(this).css('display', 'none');

        $(this).closest('.review-box').find('input[type=radio]').attr('disabled', false);
    });

    $('.user-review .cancel').click(function() {
        $(this).closest('.review-box').find('.title').attr('readonly', true);
        $(this).closest('.review-box').find('.body').attr('readonly', true);
        $(this).siblings('.save').css('display', 'none');
        $(this).css('display', 'none');

        $(this).siblings('.delete').css('display', 'flex');
        $(this).siblings('.edit').css('display', 'flex');

        $(this).closest('.review-box').find('.title').val(prevTitle);
        $(this).closest('.review-box').find('.body').val(prevBody);

        $(this).closest('.review-box').find('input[type=radio]').attr('disabled', true);

        $(this).closest('.review-box').find(`input[type=radio][value=${prevScore}]`).click();
    });
});