sec_dict = {'경제': 101, 'IT': 105}
eco_dict = {'증권': 258, '금융': 259, '부동산': 260, '산업/재계': 261,
                '글로벌 경제': 262, '경제 일반': 263, '생활경제': 310, '중기/벤처': 771}
it_dict = {'모바일': 731, '인터넷/SNS': 226, '통신/뉴미디어': 227, 'IT 일반': 230, '보안/해킹': 732, '컴퓨터': 283, '게임/리뷰': 229, '과학 일반': 228}
child_sec_dict = {101: eco_dict, 105: it_dict}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

params_init = {'ticket': 'news',
 'templateId': 'default_it',
 'pool': 'cbox5',
#  '_cv': '20240903144034',
#  '_callback': 'jQuery33101711803272944905_1725349376637',
 'lang': 'ko',
 'country': 'KR',
#  'objectId': 'news092,0002300844',
 'categoryId': '',
 'pageSize': '20',
 'indexSize': '10',
 'groupId': '',
 'listType': 'OBJECT',
 'pageType': 'more',
 'page': '1',
 'initialize': 'true',
 'followSize': '5',
 'userType': '',
 'useAltSort': 'true',
 'replyPageSize': '20',
 'sort': 'favorite',
 'includeAllStatus': 'true',
#  '_': 'p_time'
 }

params_more = {
    "ticket": "news",
    "templateId": "default_it",
    "pool": "cbox5",
    # "_cv": "20240903144034",
    # "_callback": "jQuery33101711803272944905_1725349376637",
    "lang": "ko",
    "country": "KR",
    # "objectId": "news092,0002300844",
    "categoryId": "",
    "pageSize": 20,
    "indexSize": 10,
    "groupId": "",
    "listType": "OBJECT",
    "pageType": "more",
    "page": 2,
    # "currentPage": 1,
    "refresh": False,
    "sort": "FAVORITE",
    # "current": 799229404260597805,
    # "prev": 799229205719023626,
    "moreParam.direction": "next",
    # "moreParam.prev": "100000m00000o062lj3we6iz2i",
    # "moreParam.next": "0zik0zh000004062lj6flp1y5p",
    "includeAllStatus": True,
    # "_": 'p_time'
}


params_reply = {
    'ticket': 'news',
    'templateId': 'default_it',
    'pool': 'cbox5',
    # '_cv': '20240903144034',
    # '_callback': 'jQuery33104664029422256555_1725368699648',
    'lang': 'ko',
    'country': 'KR',
    # 'objectId': 'news003,0012757566',
    'categoryId': '',
    'pageSize': '20',
    'indexSize': '10',
    'groupId': '',
    'listType': 'OBJECT',
    'pageType': 'more',
    'parentCommentNo': '835690205917741152',
    'page': '1',
    'userType': '',
    'includeAllStatus': 'true',
    'moreType': 'next',
    'sort': 'FAVORITE',
    # '_': '1725368699658'
    }
