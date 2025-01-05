# LearnMate: Your Personalized Study Assistant

---

Welcome to **LearnMate**, a powerful, AI-driven tool to help you organize your study schedules, get personalized learning tips, and achieve academic success. This repository contains the source code for the LearnMate project, split into two main parts: the **frontend** (user interface) and the **backend** (AI-powered engine).

---

## Features

- **Customizable Study Plans**: Generate personalized schedules based on your needs.
- **Learning Assistance**: Get advice on the best study methods and practices.
- **AI-Powered Insights**: Answer queries and interact with a smart assistant for real-time learning help.
- **Seamless User Experience**: Intuitive interface for smooth navigation.

---

## Project Structure

- **Frontend**: Built using modern web technologies for a responsive and user-friendly interface.
- **Backend**: Powered by LangGraph and Python, providing the AI capabilities and query handling.

---

## Prerequisites

Make sure you have the following installed on your system:

- **Node.js** (for frontend development)
- **Python 3.9+** (for backend development)
- **Poetry** (if using for dependency management in the backend)
- **Docker** (optional for containerized deployment)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Rishikesh63/learnmate.git
cd learnmate
```

---

### 2. Frontend Setup

Navigate to the `frontend` folder and install dependencies:

```bash
cd frontend
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend will start at `http://localhost:3000` by default.

---

### 3. Backend Setup

Navigate to the `backend` folder and set up the environment:

```bash
cd backend
```

- Install Python dependencies using Poetry :
  ```bash
  poetry install


- Run the backend server:
  ```bash
  uvicorn my_agent.demo:app --reload
  ```

The backend will start at `http://127.0.0.1:8000` by default.

---

## Usage

1. Start the **backend server** first (`uvicorn`).
2. Start the **frontend development server** (`npm run dev`).
3. Open your browser and navigate to `http://localhost:3000` to interact with LearnMate.

---

## Contributing

We welcome contributions to LearnMate! Feel free to fork this repository, create feature branches, and submit pull requests. Make sure to follow the contribution guidelines.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Let’s Learn Together!

Feel free to reach out with questions or feedback. Let’s build your path to success with **LearnMate**! 🚀
