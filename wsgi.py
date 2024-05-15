from gamechanger import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3181, debug=False)
else:
    application = app