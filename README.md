# Project Trivia 

## Installation & COnfiguration

The project Trivia is a full stack application with a backend in python flask and a front-end in React.

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details about installation and configuration.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?


> View the [Frontend README](./frontend/README.md) for more details.

## API Documentation

### Getting Started
- __Host:__ At present this app can only be run locally, The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- __Base URL:__  The base URL for the backend is  __/api/v1__. 
- ___Authentication:__ This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "error": 400,
    "message": "bad request",
    "success": false
}
```
The API will return four(4) error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable


### Endpoints 
#### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

- Sample: `curl http://127.0.0.1:5000/api/v1/categories`

``` json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET /categories/${id}/questions
- General:
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: `id` - integer
    - Returns: An object with questions for the specified category, total questions, and current category string
- `curl 'http://localhost:5000/api/v1/categories/4/questions'`
```json
{
    "current_category": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

#### GET /questions?page=${integer}
- General:
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    - Request Arguments: `page` - integer, default page is 1.
    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- `curl 'http://localhost:5000/api/v1/questions?page=2'`

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science",
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```
#### POST /questions
- General:
    - Sends a post request in order to add a new question
- Request Body:
```json
{
    "question": "Heres a Another Amother question string",
    "answer": "Heres a new answer string",
    "difficulty": 1,
    "category": 3
}
```
`curl --request POST 'http://localhost:5000/api/v1/questions' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "Heres a Another Amother question string",
    "answer": "Heres a new answer string",
    "difficulty": 1,
    "category": 3
}'`
- Response :
```json
{
    "success": true
}
```

#### POST /questions
- General:
    - Search a question by terms as a substring on question
- Request Body:
```json
{
  "searchTerm": "Hematology" 
}
```
`curl --request POST 'http://localhost:5000/api/v1/questions' \
--header 'Content-Type: application/json' \
--data-raw '{
  "searchTerm": "Hematology" 
}'`
- Response :
```json
{
    "current_category": "Science",
    "questions": [
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

#### DELETE /api/v1/questions/${id}
- General:
    - Delete a specific questions by id 

`curl --request DELETE 'http://localhost:5000/api/v1/questions/25'`
- Response :
```json
{
    "deleted": 25,
    "success": true
}
```

#### POST /api/v1/quizzes
- General:
    -  Get questions to play the quizze
- Request Body:
```json
{
    "previous_questions": [22, 21],
    "quiz_category": {
        "id": 1,
        "type": "Science"
    }
 }
```
`curl --request POST 'http://localhost:5000/api/v1/quizzes' \
--header 'content-type: application/json' \
--data-raw '{
    "previous_questions": [22, 21],
    "quiz_category": {
        "id": 1,
        "type": "Science"
    }
 }'`
- Response :
```json
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```
