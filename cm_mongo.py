from startup import mongo
from cm_config import DB_NAME


def test_db():
    try:
        mongo[DB_NAME].command('ping')
        return ("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        return (e)
