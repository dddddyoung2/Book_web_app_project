from book_app import db

class Review(db.Model):
    __tablename__ = 'review' #명시되어 있지 않으면 class 이름의 소문자로 자동 생성됨

    id = db.Column(db.Integer, primary_key=True)
    w_review = db.Column(db.TEXT)
    name = db.Column(db.VARCHAR)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    

    def __repr__(self):
        return f"Review {self.id}"