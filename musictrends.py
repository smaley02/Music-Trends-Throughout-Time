import PySimpleGUI as sg

import csv
import random
import time


# only needed to be used once
# def create_decade_files():
#     # creates the decade.txt files
#     # this opens the artists.csv file and extracts all the data pertaining to a particular decade, then
#     # saves the artist and decade to a txt file
#     with open('artists.csv', encoding='Latin-1') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line = 0
#         for row in csv_reader:
#             temp = ''
#             tag_num = 0
#             for tag in row[6]:
#                 genre = ''
#                 if tag == ";":
#                     if temp == " 50s" or temp == "50s":
#                         for genre_char in row[6]:
#                             if genre_char == ";":
#                                 break
#                             genre += genre_char
#                         with open('50s.csv', 'a', newline='') as test1:
#                             try:
#                                 test1.write(row[1])
#                                 test1.write("," + genre)
#                                 test1.write("," + row[8])
#                                 test1.write('\n')
#                             except UnicodeEncodeError:
#                                 print("Unicode Error")
#                             test1.close()
#
#                     if temp == " 60s" or temp == "60s":
#                         for genre_char in row[6]:
#                             if genre_char == ";":
#                                 break
#                             genre += genre_char
#                         with open('60s.csv', 'a', newline='') as test2:
#                             try:
#                                 test2.write(row[1])
#                                 test2.write("," + genre)
#                                 test2.write("," + row[8])
#                                 test2.write('\n')
#                             except UnicodeEncodeError:
#                                 print("Unicode Error")
#                             test2.close()
#
#                     if temp == " 70s" or temp == "70s":
#                         for genre_char in row[6]:
#                             if genre_char == ";":
#                                 break
#                             genre += genre_char
#                         with open('70s.csv', 'a', newline='') as test3:
#                             try:
#                                 test3.write(row[1])
#                                 test3.write("," + genre)
#                                 test3.write("," + row[8])
#                                 test3.write('\n')
#                             except UnicodeEncodeError:
#                                 print("Unicode Error")
#                             test3.close()
#
#                     if temp == " 80s" or temp == "80s":
#                         for genre_char in row[6]:
#                             if genre_char == ";":
#                                 break
#                             genre += genre_char
#                         with open('80s.csv', 'a', newline='') as test4:
#                             try:
#                                 test4.write(row[1])
#                                 test4.write("," + genre)
#                                 test4.write("," + row[8])
#                                 test4.write('\n')
#                             except UnicodeEncodeError:
#                                 print("Unicode Error")
#                             test4.close()
#
#                     if temp == " 90s" or temp == "90s":
#                         for genre_char in row[6]:
#                             if genre_char == ";":
#                                 break
#                             genre += genre_char
#                         with open('90s.csv', 'a', newline='') as test5:
#                             try:
#                                 test5.write(row[1])
#                                 test5.write("," + genre)
#                                 test5.write("," + row[8])
#                                 test5.write('\n')
#                             except UnicodeEncodeError:
#                                 print("Unicode Error")
#                             test5.close()
#
#                     if temp == " 00s" or temp == "00s":
#                         for genre_char in row[6]:
#                             if genre_char == ";":
#                                 break
#                             genre += genre_char
#                         with open('00s.csv', 'a', newline='') as test6:
#                             try:
#                                 test6.write(row[1])
#                                 test6.write("," + genre)
#                                 test6.write("," + row[8])
#                                 test6.write('\n')
#                             except UnicodeEncodeError:
#                                 print("Unicode Error")
#                             test6.close()
#                     temp = ''
#                 else:
#                     temp += tag
#             line += 1
#         csv_file.close()


class Artist:
    def __init__(self, name, genre, popularity):
        self.name = name
        self.genre = genre
        self.popularity = popularity


# decade input must be in the form "50s", "60s", "70s", etc.
def create_decade_list(decade):
    filename = decade + ".csv"
    decade_list = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            try:
                name = Artist(row['artist'], row['genre'], int(row['popularity']))
                decade_list.append(name)
            except:
                print("Error on line " + str(line_count))
            line_count += 1
        csv_file.close()
    return decade_list


# quicksort algorithm recursion
def quicksort(arr, min, max):
    if min < max:
        pivot = arr[max]
        i = min - 1
        for j in range(min, max):
            if arr[j].popularity <= pivot.popularity:
                i = i + 1
                # swap
                (arr[i], arr[j]) = (arr[j], arr[i])
        (arr[i + 1], arr[max]) = (arr[max], arr[i + 1])
        pivot = i + 1
        quicksort(arr, min, pivot - 1)
        quicksort(arr, pivot + 1, max)


# shell sort algorithm, n is inputted as array length
def shellsort(arr, n):
    gap = n // 2
    while gap > 0:
        j = gap
        while j < n:
            i = j - gap
            while i >= 0:
                if arr[i + gap].popularity > arr[i].popularity:
                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]
                i = i - gap
            j += 1
        gap = gap // 2


# returns all unique genres from a inputted genres array
def get_genres(arr):
    genres = {}
    line_count = 0
    for artist in arr:
        already_present = 0
        # see if genre is already in dict, add popularity to existing genre
        for genre in genres:
            if artist.genre == genre:
                total = artist.popularity + genres.get(genre)
                genres.update({genre: total})
                already_present = 1
        # if a unique genre, add to dict
        if already_present != 1:
            genres[artist.genre] = artist.popularity
        line_count += 1
    for genre in genres:
        # if a number is present in the genre remove it (i.e. 80s, 70s, 60s, etc.)
        if any(char.isdigit() for char in genre):
            genres.update({genre: 0})
        line_count += 1

    return genres


# get top genres
def top_genres(genres):
    top = []
    for genre in genres:
        temp = Artist(genre, genre, int(genres.get(genre)))
        top.append(temp)
    quicksort(top, 0 , len(top) - 1)

    return top


def main():
    # create a list of class Artist and shuffle the values
    fifties = create_decade_list("50s")
    sixties = create_decade_list("60s")
    seventies = create_decade_list("70s")
    eighties = create_decade_list("80s")
    ninties = create_decade_list("90s")
    twothousands = create_decade_list("00s")
    all_list = fifties + sixties + seventies + eighties + ninties + twothousands

    sg.theme('LightBrown2')

    frame_layout = [
        [sg.Text('Current Sort: '), sg.Text(size=(15, 1), key="-SORT-"),
         sg.Text('Current era: '), sg.Text(size=(15, 1), key="-ERA-"),
         sg.Button('Execute'), sg.Text(size=(35, 1), key="-TIME-")],
        [sg.Graph(canvas_size=(1000, 500),
                  graph_bottom_left=(0, 0),
                  graph_top_right=(1200, 600),
                  enable_events=True,
                  background_color='lightgrey',
                  key='-GRAPH-',
                  pad=10)]
    ]

    layout = [
        [sg.Text('Please select a decade to analyze:'),
         sg.Text(size=(15, 1), key='-OUTPUT-')],
        [sg.Button('1950s'), sg.Button('1960s'), sg.Button('1970s'), sg.Button('1980s'),
         sg.Button('1990s'), sg.Button('2000s'), sg.Button('All Decades'), sg.Button('Exit')],
        [sg.Button('Quick Sort'), sg.Button('Shell Sort')],
        [sg.Frame('Data', frame_layout, font='Any 12', title_color='white')]
    ]

    window = sg.Window('Music Trends', layout, finalize=True)

    sort = ''
    arr = []

    while True:
        event, values = window.read()
        print(event, values)

        if event in (None, 'Exit'):
            break

        if event == '1950s':
            window['-ERA-'].update('50s')
            arr = fifties
        if event == '1960s':
            window['-ERA-'].update('60s')
            arr = sixties
        if event == '1970s':
            window['-ERA-'].update('70s')
            arr = seventies
        if event == '1980s':
            window['-ERA-'].update('80s')
            arr = eighties
        if event == '1990s':
            window['-ERA-'].update('90s')
            arr = ninties
        if event == '2000s':
            window['-ERA-'].update('00s')
            arr = twothousands
        if event == 'All Decades':
            window['-ERA-'].update('All time')
            arr = all_list

        if event == 'Quick Sort':
            window["-SORT-"].update("Quick")
            sort = 'quick'
        if event == 'Shell Sort':
            window["-SORT-"].update("Shell")
            sort = 'shell'

        if event == 'Execute':
            window['-GRAPH-'].erase()
            window["-GRAPH-"].draw_text("(Ranking, Genre, Popularity)", (600, 575), color='black', font=50)
            # if no option selected
            if sort == '' or arr == []:
                window["-TIME-"].update("Please make a valid selection!")
            else:
                start = time.time()
                random.shuffle(arr)
                if sort == 'quick':
                    quicksort(arr, 0, (len(arr) - 1))
                if sort == 'shell':
                    shellsort(arr, len(arr))
                genres = get_genres(arr)
                top = top_genres(genres)
                end = time.time()
                time_elapsed = end - start
                window["-TIME-"].update("Time elapsed: " + str(time_elapsed) + " seconds")
                count = 0
                x, y = 1000, 60
                # draw artists to the graph object in three columns
                for artist in top:
                    if len(genres) - 1 - count < 30:
                        print(f'{artist.name} | popularity: {artist.popularity}')
                        string = (f'{len(genres) - count}. {artist.name} | {artist.popularity}')
                        window["-GRAPH-"].draw_text(string, (x, y), color='black', font=50)
                        y += 50
                        if len(genres) - 1 - count == 20:
                            x = 600
                            y = 60
                        if len(genres) - 1 - count == 10:
                            x = 200
                            y = 60
                    count += 1

    window.close()


if __name__ == '__main__':
    main()
