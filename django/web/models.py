from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(primary_key=True)

    def __str__(self) -> str:
        return f"(tmdb_id {self.tmdb_id})"


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    movie = models.ManyToManyField(Movie)

    models.UniqueConstraint(fields=['user', 'movie'], name='composite_key')

    def __str__(self) -> str:
        return f"(user {self.user}, movie {self.movie})"


class Favlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    movie = models.ManyToManyField(Movie)

    models.UniqueConstraint(fields=['user', 'movie'], name='composite_key')

    def __str__(self) -> str:
        return f"(user {self.user}, movie {self.movie})"


class Review(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f"(title {self.title}, content {self.content})"


class ReviewVote(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    value = models.BooleanField()  # True == upvote, False == downvote

    models.UniqueConstraint(fields=['rating', 'user'], name='composite_key')

    def __str__(self) -> str:
        return f"(user {self.user}, review {self.review}) -> {self.value}"


class Rating(models.Model):
    RATING_CHOICES = [(1, "1 star"), (2, "2 stars"),
                      (3, "3 stars"), (4, "4 stars"), (5, "5 stars")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_index=True)

    score = models.PositiveIntegerField(default=0, choices=RATING_CHOICES)

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, blank=True, null=True)

    models.UniqueConstraint(fields=['user', 'movie'], name='composite_key')

    def __str__(self) -> str:
        return f"(user {self.user}, movie {self.movie}) -> {self.score} stars"
