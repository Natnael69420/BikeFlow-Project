# BikeFlow Project

**BikeFlow – Bicycle Service Management System**

University Engineering Project

## 1. Project Overview

BikeFlow is a bicycle service management system designed to manage repair orders, customer information, bicycle details and repair progress.

The system allows users to register repair orders, retrieve existing orders, search for customers and update repair statuses.

## 2. Technologies Used

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **API:** REST API using JSON
- **Version Control:** Git and GitHub

## 3. Project Structure

```text
BikeFlow-Project/
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   └── validators/
├── database/
│   ├── db_connection.py
│   ├── schema.sql
│   └── bikeflow.db
├── frontend/
│   ├── index.html
│   ├── orders.html
│   ├── create-order.html
│   ├── order.html
│   ├── css/
│   └── js/
├── requirements.txt
├── API_CONTRACT.md
└── README.md
```

## 4. Installation and Setup

### Requirements
- Python 3
- pip
- Git

### Install dependencies

```bash
pip install -r requirements.txt
```

### Initialize database

```bash
python -m database.db_connection
```

### Start Flask

```bash
python -m backend.app
```

Backend URL: `http://127.0.0.1:5000`

API base URL: `http://127.0.0.1:5000/api`

## 5. Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Check API availability |
| POST | /api/orders | Create repair order |
| GET | /api/orders | Retrieve all orders |
| GET | /api/orders/{id} | Retrieve one order |
| GET | /api/orders/search?customer_name=Anna | Search by customer |
| PATCH | /api/orders/{id}/status | Update status or cancel |
| GET | /api/orders/{id}/history | Retrieve status history |
| GET | /api/orders/status-transitions | Retrieve permitted transitions |

## 6. Business Workflow

The backend enforces permitted status transitions.

| Current status | Permitted next status |
|---|---|
| Registered | Scheduled, Cancelled |
| Scheduled | In Progress, Cancelled |
| In Progress | Waiting for Parts, Completed, Cancelled |
| Waiting for Parts | In Progress, Cancelled |
| Completed | None |
| Cancelled | None |

### Implemented business rules

1. Only permitted status transitions are accepted.
2. Completed orders cannot return to earlier repair stages.
3. Cancelled orders cannot return to the normal repair workflow.
4. Repeating the current status does not create duplicate history entries.

Invalid transitions are rejected by the backend with HTTP 400.

## 7. Database

The application uses SQLite for persistent storage.

Current tables:

- `repair_orders` – stores repair order and customer/bicycle information.
- `status_history` – stores status changes and timestamps.

Foreign key enforcement is enabled.

## 8. Validation and Testing

### Laboratory 8

| Test | Expected result | Actual result |
|---|---|---|
| Missing customer name | HTTP 400 | Passed |
| Missing customer phone | HTTP 400 | Passed |
| Empty JSON request | HTTP 400 | Passed |
| Malformed JSON | HTTP 400 | Passed |
| Invalid submissions | No records created | Passed |

The database contained six orders before and after invalid submission testing.

### Laboratory 9

Verified functionality:
- Create repair orders.
- Retrieve all orders.
- Retrieve individual orders.
- Search by customer name.
- Update repair status.
- Retrieve status history.
- Verify persistence after restarting Flask.

**Pending:** Editing customer and bicycle details requires a database update function from the database developer.

### Laboratory 10

| Test | Expected result | Actual result |
|---|---|---|
| In Progress → Waiting for Parts | Accepted | Passed |
| Waiting for Parts → In Progress | Accepted | Passed |
| Completed → Registered | Rejected | Passed |
| Registered → Cancelled | Accepted | Passed |
| Cancelled → Scheduled | Rejected | Passed |
| Retrieve nonexistent order | HTTP 404 | Passed |
| Update nonexistent order | HTTP 404 | Passed |
| Repeat current status | No duplicate history | Passed |

## 9. Current Implementation Status

### Implemented
- Flask backend and REST API.
- SQLite integration.
- Repair order creation and retrieval.
- Customer-name search.
- Server-side validation.
- Status updates and workflow restrictions.
- Status history.
- Cancellation through status updates.
- Persistent data storage.
- Backend/frontend integration testing.

### Remaining
- Editing existing repair order details.
- Final frontend integration of editing.
- Complete documented laboratory test records.
- Final verification against the team's agreed TO-BE BPMN and Lab 4 requirements.

## 10. Team Responsibilities

- **Natnael – Backend Developer:** Flask API, validation, business logic, workflow implementation and backend testing.
- **Augsta – Frontend Developer:** HTML, CSS, JavaScript, user interface and frontend/API integration.
- **Soheib – Database Developer:** SQLite database, schema, database operations and persistence.

## 11. Repository

GitHub: https://github.com/Natnael69420/BikeFlow-Project

