from flask import Flask, render_template, request
from io import BytesIO, StringIO
from matplotlib import pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from scipy.cluster.hierarchy import dendrogram, linkage

import csv
import numpy as np
import requests
import sys

# https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/

app = Flask(__name__)

def get_google_sheets_csv_url(u):
    """
    e.g. https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/edit?usp=sharing
    to-  https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/gviz/tq?tqx=out:csv
    """
    pieces = u.split('/')[:6]
    # pieces.append('gviz')
    # pieces.append('tq?tqx=out:csv')
    pieces.append('export?format=csv')
    return '/'.join(pieces)

def get_hex(value, max_value):
    """
    0 -> #ffffff
    3 -> #666666
    """
    r = float(value) / float(max_value)
    h =  hex(int(255 - (128.0 * r))).upper()[2:]
    return 'FF{0}{0}'.format(h)
  

@app.route("/")
def form():
    """
    Display a webform to the user.
    """
    return render_template('form.html')

@app.route("/cluster", methods=["POST"])
def cluster():
    # url = request.form["url"]
    url = 'https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/edit?usp=sharing'
    url = get_google_sheets_csv_url(url)

    # r = requests.head(url, allow_redirects=True)
    csv_string = requests.get(url).text

    # catch errors: the url might not be public. 
    if '<!DOCTYPE html>' in csv_string:
        print('not public!')

    f = StringIO(csv_string)
    reader = csv.reader(f, delimiter=",")

    headings_1 = next(reader)[1:]
    headings_2 = []
    data = []

    # input data...
    # cells should be an empty string ('') if data was missing or not an
    # integer, or an integer.
    for row in reader:
        headings_2.append(row[0])
        tmp_row = []
        for cell in row[1:]:
            if cell == '':
                tmp_row.append(cell)
            else:
                try:
                    tmp_row.append(int(cell))
                except ValueError:
                    tmp_row.append('')
        data.append(tmp_row)

    # labels must be in the right orders, in the right positions.  
    assert headings_1 == headings_2 

    # get the maximum value from the input data.
    max_value = 0
    for y in range(len(data)):
        for x in range(len(data)):
            try:
                if data[y][x] > max_value:
                    max_value = data[y][x]
            except TypeError:
                pass

    # "fill in" the input data. 
    # set the diagonal to the max value.
    # if cells are empty, set them to zero.
    # if a corresponding cell has a value, copy it's value to this cell.
    # if cells have different values, set them to zero.
    y = 0
    while y < len(data):
        x = 0
        while x <= y:
            if x == y:
                data[y][x] = max_value

            if data[y][x] == '' and data[x][y] == '':
                data[y][x] = 0
                data[x][y] = 0
            elif data[y][x] == '':
                data[y][x] = data[x][y]
            elif data[x][y] == '':
                data[x][y] = data[y][x]
            elif data[y][x] != data[x][y]:
                data[y][x] = 0
                data[x][y] = 0
            x += 1
        y += 1

    # or 'complete'
    l = linkage(data, 'single')
    d = dendrogram(l) 

    # sort the matrix based on dendrogram order.
    data_out = []
    for y in range(len(data)):
        row_out = []
        for x in range(len(data)):
            row_out.append(data[d['leaves'][y]][d['leaves'][x]])
        data_out.append(row_out)

    # make an xlsx spreadsheet here to download. 
    wb = Workbook()
    ws = wb.active
    for y in range(len(data_out)):            
        for x in range(len(data_out)):            
            cell = ws.cell(row=y+2, column=x+2, value=data_out[y][x])
            print(get_hex(data_out[y][x], max_value))
            color = get_hex(data_out[y][x], max_value)
            cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

    for i in range(len(data_out)):
        ws.cell(row=1, column=i+2, value=headings_1[d['leaves'][i]])
        ws.cell(row=i+2, column=1, value=headings_1[d['leaves'][i]])

    f = BytesIO()
    wb.save(f)
    send_file(f, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
