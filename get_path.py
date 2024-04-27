from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_path(database_name):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Select all pathnames from file_paths table
    cursor.execute("SELECT pathname FROM file_paths")
    paths = [row[0] for row in cursor.fetchall()]  # Fetch all pathnames and store in a list

    conn.close()  # Close database connection
    return paths  # Return list of pathnames

# Function to fetch file details from the database
def get_file_details(file_path):
    connection = sqlite3.connect('path.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM file_paths WHERE pathname=?", (file_path,))
    file_details = cursor.fetchone()
    connection.close()
    return file_details

# Route to handle rendering HTML page with file details
@app.route('/')
def index():
    # Get pathnames from the database
    pathnames = get_path('path.db')
    return render_template('test.html', pathnames=pathnames)

# Route to handle fetching file details
@app.route('/get_file_details')
def get_file_details_route():
    selected_file = request.args.get('file')
    if selected_file:
        file_details = get_file_details(selected_file)
        if file_details:
            # Constructing the response JSON with file details
            response = {
                'fileName': selected_file,
                'size': '',  # You can add size if available in your database
                'type': '',  # You can add file type if available in your database
                'lastModified': '',  # You can add last modified if available in your database
                # Add more details as needed
            }
            return jsonify(response)
        else:
            return jsonify({'error': 'File details not found'})
    else:
        return jsonify({'error': 'No file selected'})

if __name__ == '__main__':
    app.run(debug=True)