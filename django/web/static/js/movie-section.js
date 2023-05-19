$(document).on('submit', '#review-form', e => {
    const urls = JSON.parse(document.getElementById('urls').textContent);

    e.preventDefault();

    const elem = $(e.currentTarget);

    const title = $('#id_title').val();
    const content = $('#id_content').val();
    const url = $(e.currentTarget).attr('action');

    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
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
        statusCode: {
            401: () => { 
                window.location.href = `${urls['login']}?next=${window.location.pathname}`;
            }
        },
        success: data => {
            console.log("success");
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
});