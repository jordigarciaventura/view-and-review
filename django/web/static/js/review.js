document.addEventListener('DOMContentLoaded', () => {
    const downVotes = document.querySelectorAll('.downvote');
    const upVotes = document.querySelectorAll('.upvote');

    downVotes.forEach(downVote => {
        downVote.addEventListener('click', e => {
            const target = e.currentTarget;
            const reviewId = target.parentElement.dataset['ratingId'];
            
            const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                type:  (watchlist) ? 'POST' : 'POST',
                url:`/watchlist/`,
                beforeSend: function (xhr){
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                data: {
                    'movie_id': movieID
                },
                statusCode: {
                    401: () => { 
                        window.location.href = `/accounts/login/?next=${window.location.pathname}`;
                    }
                },
                success: data => {
                    console.log("success");
                    target.data('watchlist', !watchlist);
                    target.children().toggleClass('hidden');
                }
            });
        });
    });
});