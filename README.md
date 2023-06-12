# Social-media-api
Simple Social media api that support features like getting a user profile, follow a user, upload a post, delete a post, like a post, unlike a liked post, and comment on a post.

## Features

- User authentication: Users can authenticate using their email and password, and receive a JWT token for authorization.
- User profiles: Users can view their own profile, which includes their username, number of followers, and number of followings.
- Follow/unfollow users: Authenticated users can follow or unfollow other users.
- Posts: Users can create new posts, delete their own posts, and retrieve posts with associated likes and comments.
- Likes: Users can like or unlike posts.
- Comments: Users can add comments to posts.
- Post retrieval: Users can retrieve all posts created by themselves, sorted by post time.
- Database: Supports both PostgreSQL and MongoDB as database options.
- Paginated response : All requests return a paginated and sorted response. 

## Setup

To set up the project locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/mathuranish/Social-media-api.git
```
2. Set up a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

- For PostgreSQL: Configure the database settings in settings.py and run migrations using python manage.py migrate.
```bash
python manage.py migrate
```

. Start the development server:

- Install Docker on your system by following the official Docker documentation.
- Build the Docker image:
```bash
docker build -t social-media-api .
```
- Run the Docker container:
```bash
docker-compose up
```

5. Access the API endpoints at 'http://localhost:8000/'

## API Endpoints 

- POST /api/register: Performs user registration.
Input: Email, Name ,Password ,About

- POST /api/login: Performs user Authentication and returns a JWT token.
Input: Email ,Password
Return: refresh and access Tokens

- POST token/verify/ and token/refresh/ can be used to refresh and very tokens.

- POST /user/follow/: Authenticated user follows the user with the specified following_user_id.
Input: user_id , following_user_id

POST /user/unfollow/: Authenticated user unfollows the user with the specified following_user_id.
Input: user_id , following_user_id

GET /api/user: Authenticates the request and returns the users profile.
Return: User ID, User Name, About, Number of Followers, Number of Followings, Created Time (UTC)

POST /api/post/: Adds a new post created by the authenticated user.
Input: User, Title, Description
Return: Post ID, User, Title, Description, Created Time (UTC)

GET /api/post/: Returns all posts created by the authenticated user, sorted by post time.

POST /api/like/: Likes the post by the authenticated user.
Input: Post Id

POST /api/unlike/: Unlikes the post with the specified id by the authenticated user.
Input: Post Id

POST /api/comment/: Adds a comment for the post with the specified id by the authenticated user.
Input: Post Id, Comment
Return: Comment Id, Post Id, Text

All endpoints have POST,GET, PUT, DELETE, PATCH functionality.
