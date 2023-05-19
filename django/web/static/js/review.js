document.addEventListener('DOMContentLoaded', () => {
    const urls = JSON.parse(document.getElementById('urls').textContent);

    const downVotes = document.querySelectorAll('.downvote');
    downVotes.forEach(downVote => {
        downVote.addEventListener('click', e => {
            const downVoteElem = e.currentTarget;
            const upVoteElem = downVoteElem.parentElement.querySelector('.upvote');
            const votesElem = downVoteElem.parentElement.querySelector('.votes');
            const votes = parseInt(votesElem.textContent);

            const hasDownVote = downVoteElem.classList.contains('active');
            const hasUpVote = upVoteElem.classList.contains('active');

            const httpMethod = (hasDownVote) ? 'DELETE' : (hasUpVote) ? 'PUT' : 'POST';
            const reviewId = downVoteElem.parentElement.dataset['reviewId'];
            
            const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                type: httpMethod,
                url: urls['review-vote'],
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                data: {
                    'value': false,
                    'review': reviewId
                },
                statusCode: {
                    401: () => { 
                        window.location.href = `${urls['login']}?next=${window.location.pathname}`;
                    }
                },
                success: data => {
                    if (httpMethod === 'PUT') {
                        upVoteElem.classList.toggle('active');
                        votesElem.textContent = votes - 2;
                    } else if (httpMethod === 'POST') {
                        votesElem.textContent = votes - 1;
                    } else if (httpMethod === 'DELETE') {
                        votesElem.textContent = votes + 1;
                    }

                    downVoteElem.classList.toggle('active');
                }
            });
        });
    });

    const upVotes = document.querySelectorAll('.upvote');
    upVotes.forEach(downVote => {
        downVote.addEventListener('click', e => {
            const upVoteElem = e.currentTarget;
            const downVoteElem = upVoteElem.parentElement.querySelector('.downvote');
            const votesElem = upVoteElem.parentElement.querySelector('.votes');
            const votes = parseInt(votesElem.textContent);

            const hasDownVote = downVoteElem.classList.contains('active');
            const hasUpVote = upVoteElem.classList.contains('active');

            const httpMethod = (hasUpVote) ? 'DELETE' : (hasDownVote) ? 'PUT' : 'POST';
            const reviewId = upVoteElem.parentElement.dataset['reviewId'];
            
            const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                type: httpMethod,
                url: urls['review-vote'],
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                data: {
                    'value': true,
                    'review': reviewId
                },
                statusCode: {
                    401: () => { 
                        window.location.href = `${urls['login']}?next=${window.location.pathname}`;
                    }
                },
                success: data => {
                    if (httpMethod === 'PUT') {
                        downVoteElem.classList.toggle('active');
                        votesElem.textContent = votes + 2;
                    } else if (httpMethod === 'POST') {
                        votesElem.textContent = votes + 1;
                    } else if (httpMethod === 'DELETE') {
                        votesElem.textContent = votes - 1;
                    }

                    upVoteElem.classList.toggle('active');
                }
            });
        });
    });
});