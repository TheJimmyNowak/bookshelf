from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://"

if __name__ == '__main__':
    app.run()
