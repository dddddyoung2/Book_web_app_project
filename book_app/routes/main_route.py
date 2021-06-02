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

## Review Page

#스크롤 항목으로 가져오기 --> 이름이 안떠서 실패
# @bp.route('/review', methods=["GET", "POST"])
# def review_index():
#         book_lst = Book.query.all()

#         books = [{'id':book.id, 'name':book.book_name} for book in book_lst]

#         if request.method == "POST":
#             books_name = request.form['name']
#             b = Book.query.filter(Book.book_name==books_name).first()

#         return render_template('review.html', books=books)




#--------------------------------
#library 조회
# @bp.route('/book')
# def book_index():
#         """Library 책 조회"""

#         #library 모두 조회
#         books = Book.query.all()

#         # book_list = []
#         # totalbook = 0
#         # for i in books:
#         #     book = {}
#         #     book['id'] = i.id
#         #     book['book_name'] = i.book_name
#         #     book['author'] = i.author
#         #     book['rating'] = i.rating
#         #     totalbook = sum(i.id)
#         #     book['totalbook'] = totalbook
#         #     book_list.append(book)
        
#         return render_template('book.html',books)




# #book_list
# @bp.route('/book', methods =["POST"])
# def add_book():
#         name= request.form['book_name']
#         author = request.form['author']
#         rating = request.form['rating']


        

#         try :
#             books(name)
#         except :
#             return '책 이름을 다시 확인해주세요!', 400


#         try :
#             int(rating)
#         except:
#             return '점수를 적어주세요!', 400
        
#         if int(rating) < 0 :
#             return '상상도 못한 점수 ㄴㅇㄱ', 400

#         if int(rating) > 5 :
#             return '0에서 5사이의 점수를 적어주세요.', 400

#         ######
#         #저자 자동 입력되게, scr이랑 어떻게 연결? 테이블로 만들기(cart 참고)
#         if Book.query.filter_by(book_name=name).first() :
#             return '이미 등록한 책입니다.'

#         book_code= books(name)
#         code(book_code)
        
#         a=books(name)
#         b=code(a) #책이름
#         c=code2(b) #저자이름

#         db.session.add(Book(book_name = b, author = c, rating=rating))
#         db.session.commit()

#         return redirect(url_for('book.book_index'), 400)


# @bp.route('/compare', methods=["GET", "POST"])
# def compare_index():
#     """
#     users 에 유저들을 담아 넘겨주세요. 각 유저 항목은 다음과 같은 딕셔너리
#     형태로 넘겨주셔야 합니다.
#      -  {
#             "id" : "유저의 아이디 값이 담긴 숫자",
#             "username" : "유저의 유저이름 (username) 이 담긴 문자열"
#         }

#     prediction 은 다음과 같은 딕셔너리 형태로 넘겨주셔야 합니다:
#      -   {
#              "result" : "예측 결과를 담은 문자열입니다",
#              "compare_text" : "사용자가 넘겨준 비교 문장을 담은 문자열입니다"
#          }
#     """
#     users = None
#     prediction = None

#     if request.method == "POST":
#         # POST 일 경우에 필요한 코드를 작성해 주세요
         
#         return render_template('compare_user.html', users=users, prediction=prediction)

@bp.route('/user')
def user_index():
    """
    user_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
    """

    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    user_list = None

    return render_template('user.html', alert_msg=alert_msg, user_list=user_list)
