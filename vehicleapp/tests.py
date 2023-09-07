from django.test import TestCase

# Create your tests here.


test={'source': {'id': 'the-verge', 'name': 'The Verge'},
       'author': 'Andrew J. Hawkins',
         'title': 'GM says all of its EVs will be able to power your home by 2026', 
         'description': 'GM says all of its electric vehicles will have bidirectional vehicle-to-home charging capabilities by 2026. The first EV will be the electric Chevy Silverado, due out later this year.',
           'url': 'https://www.theverge.com/2023/8/8/23823166/gm-ev-bidirectional-charging-vehicle-to-home',
             'urlToImage': 'https://cdn.vox-cdn.com/thumbor/_yGSC92PmZR3V0-vY_VN032pGbw=/0x0:2040x1360/1200x628/filters:focal(1020x680:1021x681)/cdn.vox-cdn.com/uploads/chorus_asset/file/24015542/226268_CHEVY_EV_LINEUP_PHO_ahawkins_0006.jpg',
               'publishedAt': '2023-08-08T13:00:00Z',
                 'content': 'GM says all of '}

print(test['title'])