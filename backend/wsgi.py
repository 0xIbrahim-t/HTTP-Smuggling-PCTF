from app import create_app

application = create_app()

# Disable Flask's header validation
application.config['SERVER_NAME'] = None

if __name__ == '__main__':
    # Run without header checks
    application.run(debug=True, server_name=None)