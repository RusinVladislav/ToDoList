ToDoList App is a web application built with Django REST Framework and includes a Telegram bot integration. 
The frontend is developed and provided by SkyPro.

Requirements: Python v3.10, Docker

ToDoList App provides the following functionalities:
User Authentication
Users can register and log in to the application. Additionally, users can log in using their VK (OAuth 2.0) account.
Users can update their profile information and change their passwords.
Boards, Categories, Goals and Comments
Users can create boards and add categories to them.
Within categories, users can create goals with various details, such as title, description, deadline, priority, and status.
Users can leave comments on goals.
Sharing Boards with other Users
Users can grant access to specific boards for other users based on their usernames. The shared users can have either editing or read-only access to the board.
Telegram Bot Integration
Users can verify their Telegram account by entering a verification code received from the bot in their profile settings.
Once verified, users can interact with the bot to view their goals or create new goals in existing categories, either owned by them or shared with them as editors.

Usage
After setting up the application, you can access it through the provided URLs:

Web Application: http://localhost/

API Schema (Swagger UI): http://localhost/api/schema/swagger-ui/

Please make sure to read the API documentation to understand the available endpoints and functionalities.

Note: There are some issues with the Swagger documentation at the moment.

Testing. 
To run the tests, ensure that you have pytest installed in your virtual environment. 
If you don't have it, you can install it using: pip install pytest pytest-django
