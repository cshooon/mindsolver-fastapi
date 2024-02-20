# mindsolver-fastapi

## Overview

The backend of the Diary Creation Application is built using FastAPI and integrates with the GPT-4 API provided by OpenAI. It is designed to receive user inputs through a RESTful API, process these inputs to generate personalized diary entries, and manage user data efficiently.

## Technology Stack

- **FastAPI**: For creating RESTful APIs with asynchronous request handling.
- **OpenAI API**: Utilizing GPT-3.5 for generating personalized diary content.
- **Python**: The backend is entirely written in Python, taking advantage of its asynchronous capabilities and extensive libraries.
- **dotenv**: For managing environment variables securely.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MindSolver/mindsolver-fastapi.git
   cd mindsolver-fastapi
   ```

2. **Set Up a Virtual Environment (Optional)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Navigate to the backend directory and run:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create an `.env` file in the `env` directory within your backend directory with the following content:

```
OPEN_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key to authenticate your requests to the GPT-4 API.

## Running the Application

1. **Start the FastAPI Server**

   Within the backend directory, start the server with the following command:

   ```bash
   uvicorn main:app --reload --port 9000
   ```

   This will start the FastAPI server on `http://localhost:9000`, making the API endpoints accessible.

## API Usage

### Creating Diary Entries

- **Endpoint**: `/diary`
- **Method**: POST
- **Description**: Receives user data and memos to generate a personalized diary entry using GPT-4.
- **Request Body**: JSON payload containing user information and a list of memos for the day.

Example request body:

```json
{
  "UserDto": {
    "GoogleID": "user123",
    "username": "John Doe",
    "age": 30,
    "gender": "Male",
    "job": "Software Engineer"
  },
  "TodayStampList": [
    {
      "GoogleID": "user123",
      "dateTime": "2023-10-05T14:30:00",
      "stamp": "Happy",
      "memoLet": "Completed a major project milestone."
    }
  ]
}
```

- **Response**: A streaming response that delivers the generated diary entry in real-time as it is being created by GPT-4.
