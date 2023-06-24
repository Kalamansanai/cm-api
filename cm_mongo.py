from startup import mongo


def test_db():
    try:
        mongo['cm_test'].command('ping')
        return ("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        return (e)
