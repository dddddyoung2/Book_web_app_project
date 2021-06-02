def msg_processor(msg_code):
    '''
    msg_processor returns a msg object with 'msg', 'type'
    where 'msg' corresponds to the message user sees
    and 'type' is the color of the alert element
    codes:
        - 0 : Successfully added to database
        - 1 : User does not exist
        - 2 : Unable to retrieve tweets
        - 3 : Successfully deleted user
		- 4 : 해당 이름을 가진 상품의 가격 정보가 없습니다. 다른 상품을 검색해 보세요. 
		- 5 : 식재료의 이름을 입력하세요.
		- 6 : 구매한 가격을 제대로 입력하세요. 
    '''

    msg_code = int(msg_code)

    msg_list = [
        (
            'Successfully added to database',
            'success'
        ),
        (
            'User does not exist',
            'warning'
        ),
        (
            'Unable to retrieve tweets',
            'warning'
        ),
        (
            'Successfully deleted user',
            'info'
        )
    ]

    return {
        'msg':msg_list[msg_code][0],
        'type':msg_list[msg_code][1]
    }