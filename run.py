from app import create_app, db

app = create_app("dev") # "dev" or "prod"

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run() # debug is not here, it is only for dev and is moved to its config
