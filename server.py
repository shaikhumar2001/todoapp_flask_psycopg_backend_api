from app import create_app
import os

app = create_app()

#for rule in app.url_map.iter_rules():
#    print(rule)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"), 
        port=os.getenv("PORT", 4000), 
        debug=(os.getenv("FLASK_ENV") == "development")
    )
