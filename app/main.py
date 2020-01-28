from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    # use CSV, to insure that participants can use it. 
    # people can save CSV from Excel, OpenOffice, 
    # 
    # can i get the data from a google sheets spreadsheet from its url?
    # https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/edit?usp=sharing
    # https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/gviz/tq?tqx=out:csv

    # https://docs.google.com/spreadsheets/d/{key}/gviz/tq?tqx=out:csv&sheet={sheet_name}

    # the url might not be public.
    # the url might not be for a spreadsheet. (e.g. it could be for a Google Doc instead.)
    # the spreadsheet might not be formatted in the correct way:
    #     labels must be in the right order, in the right positions.

    # fill out spreadsheet:
    #     only cells with numbers in them count.
    #     for every cell in the sheet, if it's blank, try to get the cell from the other side.
    #     if it's on a diagonal, set the cell to the maximum number. 
    #     if none of those things happened that cell is a zero. 

    # what format does the algorithm need the data in? 

    return "Hello World from Flask"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
