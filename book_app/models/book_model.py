from book_app import db

class Book(db.Model):
    __tablename__ = 'book' #명시되어 있지 않으면 class 이름의 소문자로 자동 생성됨

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.VARCHAR, nullable=False)
    author = db.Column(db.VARCHAR)
    rating = db.Column(db.Integer, nullable=False)

    reviews= db.relationship('Review', backref= 'book', cascade = "all, delete")

    def __repr__(self):
        return f"Book {self.id}"

    # def get_books() :
    #     return Book.query.all()