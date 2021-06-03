from itertools import count
from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask.wrappers import Response
import book_app
from book_app.models.book_model import Book
from book_app.models.review_model import Review
from book_app import db
from book_app.naver_scr import books, code, code2
from book_app.utills import main_funcs

bp = Blueprint('main', __name__)

#home
@bp.route('/')
def index():
    return render_template('index.html')


# @bp.route('/book')
# def get_books():
#     return Book.query.all()

#---------------------------------------------------------------------------------------------------#
## Library Page

#library 항목 조회(list 반환안됨)
@bp.route('/book')
def get_books():
    """Library 책 조회"""

    #library 모두 조회
    books = Book.query.all()

    book_list = []
    totalbook = 0
    for p_book in books:
        book = {}
        book['id'] = p_book.id
        book['book_name'] = p_book.book_name
        book['author'] = p_book.author
        book['rating'] = p_book.rating
        totalbook = p_book.id
        book['totalbook'] = totalbook
        book_list.append(book)
    

    return render_template('book.html',book_list=book_list, totalbook=totalbook)

#항목 추가
@bp.route('/book', methods=['POST'])
def add_book():
        msg_code = request.args.get('msg_code', None)

        name= request.form['book_name']
        author = request.form['author']
        rating = request.form['rating']

        try :
            books(name)
        except :
            return '책 이름을 다시 확인해주세요!', 400


        try :
            int(rating)
        except:
            return '점수를 적어주세요!', 400
        
        if int(rating) < 0 :
            return '상상도 못한 점수! ㄴㅇㄱ', 400

        if int(rating) > 5 :
            return '0에서 5사이의 점수를 적어주세요.', 400

        
        if Book.query.filter_by(book_name=name).first() :
            return '이미 등록한 책입니다.'

        if Book.query.filter_by(book_name=name).first() == None :
            db.session.add(Book(book_name = name, author = author, rating=rating))
            db.session.commit()

        return redirect(url_for('main.add_book'))

#항목 제거
@bp.route('/book/')
@bp.route('/book/<int:id>')
def delete_book(id=None):
        """해당 id 값을 갖고 있는 목록에 담긴 책을 삭제합니다"""
        if id is None:
            return '', 400
        if Book.query.filter_by(id = id).first() is None:
            return '', 404

        else:
            p_book = Book.query.filter_by(id=id).first()
            db.session.delete(p_book)
            db.session.commit()

            return redirect(url_for('main.add_book'))

#항목 수정

#---------------------------------------------------------------------------------------------------#
## Review Page

@bp.route('/review')
def get_review():
    """리뷰 항목 조회"""

    #library 모두 조회
    reviews = Review.query.all()

    review_list = []
    for p_review in reviews:
        review = {}
        review['id'] = p_review.id
        review['name'] = p_review.name
        review['w_review'] = p_review.w_review
        review_list.append(review)
    
    return render_template('review.html',review_list=review_list)

#항목 추가
@bp.route('/review', methods=['POST'])
def add_review():
        msg_code = request.args.get('msg_code', None)

        name= request.form['name']
        w_review = request.form['w_review']

        try :
            books(name)
        except :
            return '책 이름을 다시 확인해주세요!', 400


        try :
            w_review
        except:
            return '기록할 구절을 남겨주세요!', 400

        if Review.query.filter_by(w_review=w_review).first():
            return '이미 등록한 구절입니다.'

        if Review.query.filter_by(w_review=w_review).first() == None :
            db.session.add(Review(name = name, w_review = w_review))
            db.session.commit()

        return redirect(url_for('main.add_review'))

#리뷰 제거
@bp.route('/review/')
@bp.route('/review/<int:id>')
def delete_review(id=None):
        """해당 id 값을 갖고 있는 목록에 담긴 책을 삭제합니다"""
        if id is None:
            return '', 400
        if Review.query.filter_by(id = id).first() is None:
            return '', 404

        else:
            p_review = Review.query.filter_by(id=id).first()
            db.session.delete(p_review)
            db.session.commit()

            return redirect(url_for('main.add_review'))


#리뷰 수정
@bp.route('/reviewupdate/')
@bp.route('/reviewupdate/<int:id>')
def update_review(id):
    p_review = Review.query.filter_by(id=id).first()
    return render_template('review2.html', name = p_review.name, w_review = p_review.w_review)


#/update/<int:id>
@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    up_p_review = Review(name=request.form['name'], w_review=request.form['w_review'])
    or_p_review = Review.query.filter_by(id=id).first()

    or_p_review.name = up_p_review.name
    or_p_review.w_review = up_p_review.w_review

    # up_name = or_p_review.name
    # up_review = or_p_review.w_review
    db.session.commit()
    return redirect(url_for('main.add_review'))