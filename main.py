from website import create_app

app = create_app()

if __name__ == '__main__':

    app.run(debug=True) #ensures the website refreshes every time code is changed, would not want this in production 
