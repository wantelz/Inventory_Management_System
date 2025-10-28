# Inventory Management System

A full-stack inventory management application built with Flask and React.
This project will be expanded periodically.

## Features

- 📦 Complete inventory item management (Create, Read, Update, Delete)
- 🔐 User authentication with JWT tokens
- 🔍 Search and filter items by name, description, or item code
- 📊 Dashboard with real-time statistics
- ⚠️ Low stock alerts and tracking
- 📈 Category-based organization and analytics
- 💰 Inventory value calculations

## Tech Stack

### Backend
- **Python 3.10+**
- **Flask** - Web framework
- **MongoDB Atlas** - Cloud database
- **JWT** - Authentication
- **bcrypt** - Password hashing

### Frontend
- **React 19** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization

## Prerequisites

Before running this application, make sure you have:

- **Python 3.10 or higher** installed
- **Node.js 16 or higher** and npm installed
- **MongoDB Atlas account** (free tier works fine)
- **Git** installed

## Installation & Setup

### 1. Clone the Repository

### 2. Backend Setup

#### Step 2.1: Navigate to backend directory

#### Step 2.2: Create Python virtual environment
```bash
python -m venv venv
```

#### Step 2.3: Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

#### Step 2.4: Install Python dependencies
```bash
pip install flask flask-cors flask-jwt-extended pymongo bcrypt python-dotenv
```

#### Step 2.5: Configure environment variables

Create a `.env` file in the `backend` directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your MongoDB connection string:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=YourApp
JWT_SECRET_KEY=your_super_secret_key_here_change_this_in_production
FLASK_ENV=development
```

**Getting MongoDB Atlas Connection String:**
1. Go to [MongoDB Atlas]
2. Create a free cluster
3. Click "Connect" → "Connect your application"
4. Copy the connection string and replace `<username>` and `<password>` with your database credentials

### 3. Frontend Setup

#### Step 3.1: Navigate to frontend directory
```bash
cd ../frontend
```

#### Step 3.2: Install Node.js dependencies
```bash
npm install
```

## Running the Application

You need to run **both backend and frontend** in separate terminal windows.

### Terminal 1: Start Backend Server

```bash
cd backend
.\venv\Scripts\Activate.ps1  # Activate virtual environment
python run.py
```

**Expected output:**
```
✓ MongoDB connected successfully!
 * Running on http://127.0.0.1:5000
```

Backend will run on: **http://localhost:5000**

### Terminal 2: Start Frontend Server

```bash
cd frontend
npm start
```

**Expected output:**
```
Compiled successfully!
You can now view frontend in the browser.
Local: http://localhost:3000
```

Frontend will automatically open in your browser at: **http://localhost:3000**

## Usage

### First Time Setup

1. **Register a new account**
   - Click "Register" on the login page
   - Enter username, email, and password (minimum 6 characters)
   - Click "Register"

2. **Login**
   - Enter your email and password
   - Click "Login"

3. **Add inventory items**
   - Click "Add Item" tab
   - Fill in item details:
     - Name (required)
     - Item Code (required)
     - Category (required)
     - Description (optional)
     - Quantity (required)
     - Price (required)
     - Minimum Stock Level (default: 10)
   - Click "Add Item"

4. **View and manage items**
   - Navigate to "Items" tab
   - Use search bar to find items
   - Filter by category
   - Edit or delete items as needed

5. **Monitor dashboard**
   - View "Dashboard" tab for:
     - Total items count
     - Low stock items
     - Total inventory value
     - Category breakdown

## Project Structure

```
Inventory_Management_System/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models (User, Item)
│   │   ├── routes/          # API endpoints (auth, items, stats)
│   │   └── utils/           # Utility functions
│   ├── .env                 # Environment variables (not in git)
│   ├── .env.example         # Environment template
│   ├── run.py              # Application entry point
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React UI components
│   │   ├── contexts/       # Authentication context
│   │   └── api/           # Axios configuration
│   ├── public/            # Static files
│   └── package.json       # Node.js dependencies
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Items (Requires Authentication)
- `GET /api/items/` - Get all items (with pagination & filters)
- `GET /api/items/<id>` - Get single item
- `POST /api/items/` - Create new item
- `PUT /api/items/<id>` - Update item
- `DELETE /api/items/<id>` - Delete item

### Statistics (Requires Authentication)
- `GET /api/stats/` - Get dashboard statistics
