import dash
from dash import Dash, Input, Output, callback, html, State, ctx
import flask
import dash_mantine_components as dmc

import requests
import json
import os

# api_key = os.getenv('api_key')
# url = os.getenv('url')


api_key = 'bb72b42e-760c-4535-a20e-c719a19c75f5'
url = 'https://api.random.org/json-rpc/4/invoke'


headers = {
    'Content-Type': 'application/json'
}


book_chapter_list = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66,
                     52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 3]

book_list = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1st Samuel', '2nd Samuel', '1st Kings', '2nd Kings', '1st Chronicles', '2nd Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms',
             'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
             'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1st Corinthians', '2nd Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1st Thessalonians', '2nd Thessalonians',
             '1st Timothy', '2nd Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1st Peter', '2nd Peter', '1st John', '2nd John', '3rd John', 'Jude', 'Revelation'
             ]
bible_gateway_list = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1%20Samuel', '2%20Samuel', '1%20Kings', '2%20Kings', '1%20Chronicles', '2%20Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms',
                      'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
                      'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1%20Corinthians', '2%20Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1%20Thessalonians', '2%20Thessalonians',
                      '1%20Timothy', '2%20Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1%20Peter', '2%20Peter', '1%20John', '2%20John', '3%20John', 'Jude', 'Revelation']
revelation_2_churches = ['Ephesus', 'Smryna', 'Pergamum', 'Thyatira']
revelation_3_churches = ['Sardis', 'Philadelphia', 'Laodicea']


def get_random_thing(min, max):
    params = {
        'jsonrpc': '2.0',
        'method': 'generateIntegers',
        'params': {
            'apiKey': api_key,
            'n': 1,          # Number of random integers to generate
            'min': min,        # Minimum value of the random integers
            'max': max,      # Maximum value of the random integers
            'replacement': True
        },
        'id': 1
    }

    # Make the request
    response = requests.post(url, headers=headers,
                             data=json.dumps(params))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
    return result


app = Dash(__name__)
server = app.server
app.title = 'Bible Generator'

app.layout = dmc.MantineProvider(
    dmc.Container(
        dmc.Grid(
            children=[
                dmc.Col(
                    html.H1('Book Generator'),
                    span=12
                ),
                dmc.Col(
                    children=[
                        dmc.Button(
                            'Generate me a chapter to read',
                            id='random_call_button'
                        ),
                        dmc.Text(
                            id='text_output'
                        ),
                        dmc.Select(
                            data=['NIV', 'ESV', 'NVI', 'CSB', 'NASB'],
                            value='NIV',
                            id='translation'
                        ),
                        dmc.Anchor(dmc.Button("Bible Gateway"),
                                   href="https://biblegateway.com", id='bible_link', target='_blank'),
                        dmc.Anchor(dmc.Button("Our Daily Bread"),
                                   href="https://odb.org/", id='odb', target='_blank'),
                        dmc.Anchor(dmc.Button("Random.org"),
                                   href="random.org", target='_blank'),
                        dmc.Button('Psalms', id='psalms_button')
                    ],
                    span=12
                ),
                dmc.Col(
                    dmc.Text(id='psalm')
                )
            ]
        )
    )
)


@app.callback(
    Output('text_output', 'children'),
    Output('bible_link', 'href'),
    Input('random_call_button', 'n_clicks'),
    Input('psalms_button', 'n_clicks'),
    State('translation', 'value'),
    prevent_initial_call=True
)
def get_chapter(book_click, psalm_click, translation):
    button_clicked = ctx.triggered_id
    # Define the parameters for the request
    # book_params = {
    #     'jsonrpc': '2.0',
    #     'method': 'generateIntegers',
    #     'params': {
    #         'apiKey': api_key,
    #         'n': 1,          # Number of random integers to generate
    #         'min': 64,        # Minimum value of the random integers
    #         'max': 65,      # Maximum value of the random integers
    #         'replacement': True
    #     },
    #     'id': 1
    # }

    # # Make the request
    # book_response = requests.post(url, headers=headers,
    #                          data=json.dumps(book_params))

    # # Check if the request was successful
    # if book_response.status_code == 200:
    #     # Parse the JSON response
    #     book_result = book_response.json()
    if button_clicked == 'random_call_button':
        book_result = get_random_thing(0, 65)
        book = int(book_result['result']['random']['data'][0])

        if book_chapter_list[book] == 1:
            bible_gateway_link = 'https://www.biblegateway.com/passage/?search=' + \
                bible_gateway_list[book] + '%20' + \
                ' &version=' + translation
            return str(book_list[book]) + ' 1', bible_gateway_link

        # chapter_params = {
        #     'jsonrpc': '2.0',
        #     'method': 'generateIntegers',
        #     'params': {
        #         'apiKey': api_key,
        #         'n': 1,          # Number of random integers to generate
        #         'min': 1,        # Minimum value of the random integers
        #         # Maximum value of the random integers
        #         'max': book_chapter_list[book],
        #         'replacement': True
        #     },
        #     'id': 2
        # }

        # # Make the request
        # response = requests.post(url, headers=headers,
        #                          data=json.dumps(chapter_params))

        # # Check if the request was successful
        # if response.status_code == 200:
        #     # Parse the JSON response
        #     chapter_result = response.json()

        chapter_result = get_random_thing(1, book_chapter_list[book])

        try:
            chapter = int(chapter_result['result']['random']['data'][0])
        except:
            print(chapter)
        church_chap = False
        if book == 65:
            if chapter == 2:
                church_chap = True
                church_result = get_random_thing(0, 3)
                church_num = int(
                    church_result['result']['random']['data'][0])
                church = str(revelation_2_churches[church_num])
            elif chapter == 3:
                church_chap = True
                church_result = get_random_thing(0, 2)
                church_num = int(
                    church_result['result']['random']['data'][0])
                church = str(revelation_3_churches[church_num])

        bible_gateway_link = 'https://www.biblegateway.com/passage/?search=' + \
            bible_gateway_list[book] + '%20' + \
            str(chapter) + ' &version=' + translation
        if church_chap == True:
            return str(book_list[book]) + ' ' + str(chapter) + ' - ' + church, bible_gateway_link
        else:
            return str(book_list[book]) + ' ' + str(chapter), bible_gateway_link

    elif button_clicked == 'psalms_button':
        chapter_result = get_random_thing(1, 150)
        chapter = int(chapter_result['result']['random']['data'][0])
        bible_gateway_link = 'https://www.biblegateway.com/passage/?search=' + \
            'Psalm' + '%20' + \
            str(chapter) + ' &version=' + translation
        return 'Psalm ' + str(chapter), bible_gateway_link


if __name__ == '__main__':
    app.run_server(debug=True)
