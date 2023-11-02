from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)


uri = "neo4j+ssc://5032a480.databases.neo4j.io"
username = "neo4j"
password = "password"
driver=GraphDatabase.driver(uri, auth=(username, password))


def connect():
    return driver.session()

# 1. Insert new movie information
@app.route('/imdb', methods=['POST'])
def insert_movie():
    try:
        data = request.json
        query = "CREATE (m:Movie {title: $title, description: $description, rating: $rating, revenue: $revenue})"
        params = {
            "title": data['title'],
            "description": data['description'],
            "rating": data['rating'],
            "revenue":data['revenue']
        }
        connect().run(query, params)
        return "Movie information inserted successfully", 201
    except:
        return "Movie information not inserted successfully", 404


# 2. Update movie information by title
@app.route('/imdb/<string:title>', methods=['PATCH'])
def update_movie(title):
    data = request.json
    query = "MATCH (m:Movie {title: $title}) SET m.description = $description, m.rating = $rating"
    params = {
        "title": title,
        "description": data.get('description', None),
        "rating": data.get('rating', None)
    }
    connect().run(query, params)
    return "Movie information updated successfully", 200



# 3. Delete movie information by title
@app.route('/imdb/<string:title>', methods=['DELETE'])
def delete_movie(title):
    query = "MATCH (m:Movie {title: $title}) DELETE m"
    params = {
        "title": title
    }
    connect().run(query, params)
    return "Movie information deleted successfully", 200



# 4. Retrieve all movies in the database
@app.route('/imdb', methods=['GET'])
def get_data():
    query = "MATCH (movie:Movie) RETURN movie"
    try:
        results = connect().run(query).data()
        return jsonify(results)
    except:
        return "Error Getting Results"

# 5. Display movie details including actors, directors, and genres by title
@app.route('/imdb/<string:title>', methods=['GET'])
def get_movie_details(title):
    query = "MATCH (movie:Movie {title: $title}) RETURN movie"
    params = {
        "title": title
    }
    try:
        result = connect().run(query, params)
        data = [record.data() for record in result]
        return jsonify(data)
    except:
        print("Error Fetching ",title," Movie Details")





if __name__ == '__main__':
    app.run(debug=True)
