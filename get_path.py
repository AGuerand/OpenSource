from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_path(database_name):
 
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT pathname FROM file_paths")
    paths = [row[0] for row in cursor.fetchall()] 

    conn.close() 
    return paths  


def get_file_details(file_path):
    connection = sqlite3.connect('path.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM file_paths WHERE pathname=?", (file_path,))
    file_details = cursor.fetchone()
    connection.close()
    return file_details


@app.route('/')
def index():

    pathnames = get_path('path.db')
    return render_template('test.html', pathnames=pathnames)

@app.route('/get_file_details')
def get_file_details_route():
    selected_file = request.args.get('file')
    if selected_file:
        file_details = get_file_details(selected_file)
        if file_details:
            
            response = {
                'fileName': selected_file,
                'size': '',  
                'type': '', 
                'lastModified': '',  
                
            }
            return jsonify(response)
        else:
            return jsonify({'error': 'File details not found'})
    else:
        return jsonify({'error': 'No file selected'})

if __name__ == '__main__':
    app.run(debug=True)