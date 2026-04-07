# server.py
from app import create_app
from app.config.config import Config

app = create_app()
conf = Config()

#for rule in app.url_map.iter_rules():
#    print(rule)

if __name__ == "__main__":
    app.run(
        host=conf.HOST, 
        port=conf.PORT, 
        debug=conf.DEBUG
    )
