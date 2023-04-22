from flask import Flask, jsonify
import sqlite3

def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    def db_connect(query):
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    @app.route('/movie/<title>')
    def search_by_title(title):
        query = f"""
                SELECT
                    title,
                    country,
                    release_year,
                    listed_in AS genre,
                    description
                FROM netflix
                WHERE title = '{title}'
                ORDER BY release_year DESC
                LIMIT 1 
            """
        response = db_connect(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'query': response[3],
            'description': response[4],
        }
        return jsonify(response_json)

    @app.route('/movie/<int:start>/to/<int:end>')
    def search_by_period(start,end):
        query = f"""
                        SELECT 
                             title,
                             release_year 
    
                        FROM netflix
                        WHERE release_year BETWEEN {start} AND {end}
                        LIMIT 100
                """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1]
            })
        return jsonify(response_json)

    @app.route('/rating/<group>')
    def search_by_rating(group):
        levels = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'abult': ['R', 'NC-17']
        }
        if group in levels:
            level = ', '.join([f"'{r}'" for r in levels[group]])
        else:
            return jsonify([])

        query = f"""
                SELECT 
                    title,
                    rating,
                    description

                FROM netflix 

                WHERE rating IN ({level})
        """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1],
                'description': film[2].strip()
            })
        return jsonify(response_json)

    @app.route('/genre/<genre>')
    def search_by_genre(genre):
        query = f"""
                        SELECT 
                             title,
                             description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        ORDER BY release_year DESC
                        LIMIT 10
                """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1]
            })
        return jsonify(response_json)

    def get_actors(name1='Tom Kane', name2='Alan Oppenheimer'):
        query = f""" 
               SELECT "cast"
               FROM netflix
               WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%' 
        """
        response = db_connect(query)
        actors = []
        for cast in response:
            actors.extend(cast[0].split(', '))
        result = []
        for a in actors:
            if a not in [name1, name2]:
                if actors.count(a) > 2:
                    result.append(a)
        print(result)
        #return result

    def get_films(type_film='Movie', release_year=2016, genre='Dramas'):
        query = f""" 
            SELECT 
                title,
                description
            FROM 
                netflix
            WHERE 
                "type" = '{type_film}'
                AND "release_year" = {release_year}
                AND listed_in LIKE '%{genre}%'
        """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1]
            })
        print(response_json)
    get_films()
    #get_actors()
    #app.run(debug=True)



if __name__ == '__main__':
    main()