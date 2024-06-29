import dash
from dash import Dash, Input, Output, callback, html, State
import flask
import dash_mantine_components as dmc

import requests
import json




headers = {
    'Content-Type': 'application/json'
}


book_chapter_list = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66,
                     52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

book_list = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1st Samuel', '2nd Samuel', '1st Kings', '2nd Kings', '1st Chronicles', '2nd Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms',
             'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
             'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1st Corinthians', '2nd Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1st Thessalonians', '2nd Thessalonians',
             '1st Timothy', '2nd Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1st Peter', '2nd Peter', '1st John', '2nd John', '3rd John', 'Jude', 'Revelation'
             ]
bible_gateway_list = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1%20Samuel', '2%20Samuel', '1%20Kings', '2%20Kings', '1%20Chronicles', '2%20Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms',
                      'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
                      'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1%20Corinthians', '2%20Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1%20Thessalonians', '2%20Thessalonians',
                      '1%20Timothy', '2%20Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1%20Peter', '2%20Peter', '1%20John', '2%20John', '3%20John', 'Jude', 'Revelation']


app = Dash(__name__)
server = app.server

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
                                   href="random.org", target='_blank')
                    ],
                    span=12
                )
            ]
        )
    )
)


@app.callback(
    Output('text_output', 'children'),
    Output('bible_link', 'href'),
    Input('random_call_button', 'n_clicks'),
    State('translation', 'value')
)
def get_chapter(clicks, translation):
    if clicks is not None:
        # Define the parameters for the request
        book_params = {
            'jsonrpc': '2.0',
            'method': 'generateIntegers',
            'params': {
                'apiKey': api_key,
                'n': 1,          # Number of random integers to generate
                'min': 0,        # Minimum value of the random integers
                'max': 65,      # Maximum value of the random integers
                'replacement': True
            },
            'id': 1
        }

        # Make the request
        response = requests.post(url, headers=headers,
                                 data=json.dumps(book_params))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            book_result = response.json()

        book = int(book_result['result']['random']['data'][0])

        if book_chapter_list[book] == 1:
            bible_gateway_link = 'https://www.biblegateway.com/passage/?search=' + \
                bible_gateway_list[book] + '%20' + ' &version=' + translation
            return str(book_list[book]) + ' 1', bible_gateway_link

        chapter_params = {
            'jsonrpc': '2.0',
            'method': 'generateIntegers',
            'params': {
                'apiKey': api_key,
                'n': 1,          # Number of random integers to generate
                'min': 1,        # Minimum value of the random integers
                # Maximum value of the random integers
                'max': book_chapter_list[book],
                'replacement': True
            },
            'id': 2
        }

        # Make the request
        response = requests.post(url, headers=headers,
                                 data=json.dumps(chapter_params))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            chapter_result = response.json()

        try:
            chapter = chapter_result['result']['random']['data']
        except:
            print(chapter)

        bible_gateway_link = 'https://www.biblegateway.com/passage/?search=' + \
            bible_gateway_list[book] + '%20' + \
            str(chapter[0]) + ' &version=' + translation

        return str(book_list[book]) + ' ' + str(chapter[0]), bible_gateway_link
    else:
        return "", "/"


if __name__ == '__main__':
    app.run_server(debug=True)
