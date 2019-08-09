from techex import create_app

def main():
    """driver for flask application"""
    app = create_app()
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()

    