from app import create_app, db

app = create_app("dev") # "dev" or "prod"

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run() # debug is not here, it is only for dev and is in its config


# python
# import secrets
# secrets.token_hex(16) <- generates a key string
# app.config["SECRET_KEY"] = '23c3f0c3963ae910e959ab6a4ae6ce46' # can be any string
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskapp.db" # For sqlite has to be .db
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# posts = [
#     {
#         'title': 'Test 1',
#         'content': 'Test 1 content',
#         'author': 'Meeah!'
#     },
#     {
#         'title': 'Test 2',
#         'content': 'Test 2 content',
#         'author': 'Youuh!'
#     },
#     {
#         'title': 'Test 3',
#         'content': 'Test 3 content',
#         'author': 'Sheeeh!'
#     }
# ]
# posts_empty = []

# @app.route("/about")
# def about():
#     all_posts = posts
#     # abc = "Abc"
#     # abc # "This is about us, about us"
#     return render_template("about.html", allPosts = all_posts, newTitle = "^*,..,*^")
#     # HTML code can be returned
#     # """
#     # <html>
#     # <body>
#     #     <p style="color: red"> This s HTML </p>
#     # </body>
#     # </html>
#     # """
