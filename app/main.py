import subprocess, tempfile
from flask import Flask, Response, render_template, request
from werkzeug.wsgi import FileWrapper

app = Flask(__name__)

def get_google_sheets_csv_url(u):
    """
    Convert a public URL for a Google Sheet to a URL with 'raw CSV'-
    e.g. https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/edit?usp=sharing
    to-  https://docs.google.com/spreadsheets/d/1s2Q0wC1TheZIahkw_Ly876pZUNCUZv82bVMu2A9f774/gviz/tq?tqx=out:csv
    """
    pieces = u.split('/')[:6]
    pieces.append('export?format=csv')
    return '/'.join(pieces)

def get_svg_string_from_subprocess(args):
    """
    Get a string of SVG output from a subprocess using a named temporary file.
    """
    with tempfile.NamedTemporaryFile() as f:
        args.append(f.name)
        subprocess.call(args)
        f.seek(0)
        return f.read()

def get_svg_response(svg_string, svg_filename):
    """
    Get a Flask Response to return a named SVG file.
    """
    r = Response(svg_string, mimetype="image/svg+xml", direct_passthrough=True)
    r.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(svg_filename)
    return r

@app.route("/")
def form():
    """
    Display webform.
    """
    return render_template('form.html')

@app.route("/cluster", methods=["POST"])
def cluster():
    """
    Process form submissions.
    """
    if request.form['url'] == '':
        return render_template('error.html')
    url = get_google_sheets_csv_url(request.form['url'])

    subprocess_args = {
	'dendrogram': [
            'Rscript', 
            '/app/dendrogram.r',
            request.form['linkage'], 
            url
        ],
	'graph': [
            'Rscript', 
            '/app/graph.r',
            request.form['cutoff'], 
            url
        ],
        'matrix': [
            'Rscript', 
            '/app/matrix.r',
            request.form['linkage'], 
            url
        ]
    }

    if request.form['output'] in ('dendrogram', 'graph', 'matrix'):
        try:
            return get_svg_response(
                get_svg_string_from_subprocess(
                    subprocess_args[request.form['output']]
                ),
                '{}.svg'.format(request.form['output'])
            )
        except Exception as e:
            return str(e)
    else:
        raise NotImplementedError

'''
if __name__ == "__main__":
    # debug only
    app.run(host='0.0.0.0', debug=True, port=80)
'''
