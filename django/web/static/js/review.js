$(document).ready(() => {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $('.downvote').click(e => {
        const downVoteElem = $(e.currentTarget);

        const upVoteElem = downVoteElem.siblings('.upvote');
        const votesElem = downVoteElem.siblings('.votes');

        const votes = parseInt(votesElem.text());

        const hasDownVote = downVoteElem.hasClass('active');
        const hasUpVote = upVoteElem.hasClass('active');

        const httpMethod = (hasDownVote) ? 'DELETE' : (hasUpVote) ? 'PUT' : 'POST';

        const reviewId = downVoteElem.closest('.review').data('reviewId');
        const url = downVoteElem.closest('.review').data('voteUrl');

        $.ajax({
            type: httpMethod,
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                'value': false,
                'review': reviewId
            },
            success: data => {
                if (httpMethod === 'PUT') {
                    upVoteElem.toggleClass('active');
                    votesElem.text(votes - 2);
                } else if (httpMethod === 'POST') {
                    votesElem.text(votes - 1);
                } else if (httpMethod === 'DELETE') {
                    votesElem.text(votes + 1);
                }

                downVoteElem.toggleClass('active');
            },
            error: xhr => {
                if (xhr.status == 401) {
                    redirectUrl = xhr.responseText
                    window.location.href = `${redirectUrl}?next=${window.location.pathname}`;
                }
            }
        });
    });

    $('.upVote').click(e => {
        const upVoteElem = $(e.currentTarget);
        const downVoteElem = upVoteElem.siblings('.downvote');
        const votesElem = upVoteElem.siblings('.votes');
        const votes = parseInt(votesElem.text());

        const hasDownVote = downVoteElem.hasClass('active');
        const hasUpVote = upVoteElem.hasClass('active');

        const httpMethod = (hasUpVote) ? 'DELETE' : (hasDownVote) ? 'PUT' : 'POST';

        const reviewId = upVoteElem.closest('.review').data('reviewId');
        const url = upVoteElem.closest('.review').data('voteUrl');

        $.ajax({
            type: httpMethod,
            url: url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            data: {
                'value': true,
                'review': reviewId
            },
            success: data => {
                if (httpMethod === 'PUT') {
                    downVoteElem.toggleClass('active');
                    votesElem.text(votes + 2);
                } else if (httpMethod === 'POST') {
                    votesElem.text(votes + 1);
                } else if (httpMethod === 'DELETE') {
                    votesElem.text(votes - 1);
                }

                upVoteElem.toggleClass('active');
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