# users for conftest and register tests
USER_USERNAME_1 = "ahmed"
USER_EMAIL_1 = "ahmed@example.com"
USER_PASSWORD_1 = "Str0ng-pass-123"

USER_USERNAME_2 = "omar"
USER_EMAIL_2 = "omar@example.com"
USER_PASSWORD_2 = "An0ther-pass-456"

# used in review tests and book rating test
REVIEW_RATING_1 = 4
REVIEW_TEXT_1 = "solid read"
REVIEW_RATING_2 = 5
REVIEW_TEXT_2 = "great"
REVIEW_RATING_ABOVE_MAX = 6

# fixture books for conftest and book list test
FIXTURES = ["books"]
FIXTURE_BOOKS_COUNT = 8

# used in not found tests
MISSING_ID = 999

# expected response fields in book and review tests
BOOK_DETAIL_FIELDS = {
    "id",
    "title",
    "author",
    "description",
    "avg_rating",
    "reviews_count",
    "published_date",
    "content",
}
REVIEW_FIELDS = {"id", "user", "username", "rating", "text", "created_at", "updated_at"}
