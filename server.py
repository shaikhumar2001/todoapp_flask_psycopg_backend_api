from app import create_app
from app.config.config import Config

app = create_app()
conf = Config()

#for rule in app.url_map.iter_rules():
#    print(rule)

if __name__ == "__main__":
    app.run(
        host=conf.DB_HOST, 
        port=conf.DB_PORT, 
        debug=conf.DEBUG
    )
