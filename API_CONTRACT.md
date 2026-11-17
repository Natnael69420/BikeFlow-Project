# BIKEFLOW – API CONTRACT

**Project:** Bicycle Service Management System (BSMS)  
**Business:** BikeFlow  
**Document:** API Contract  
**Version:** 1.1 (Proposed Update)  
**Previous Version:** 1.0  
**Status:** Pending team approval

## 1. Introduction

This document defines communication rules between the frontend, backend and database components of BikeFlow.

### Project architecture

1. Frontend: HTML, CSS and JavaScript.
2. Backend: Python and Flask REST API.
3. Database: SQLite.

The frontend communicates with the backend through HTTP requests. The backend validates requests, processes business logic and communicates with the database.

**Base URL:** `http://127.0.0.1:5000/api`

## 2. Data Structure

### Repair Order

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique repair order identifier |
| customer_name | String | Customer's full name |
| customer_phone | String | Customer's phone number |
| bicycle_type | String | Type of bicycle |
| bicycle_brand | String | Bicycle manufacturer |
| problem_description | String | Description of the problem |
| status | String | Current repair order status |
| created_at | DateTime | Registration date and time |

Required creation fields:
- customer_name
- customer_phone
- bicycle_type
- bicycle_brand
- problem_description

The backend generates the ID, initial status and creation timestamp.

## 3. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/orders` | Create repair order |
| GET | `/api/orders` | Retrieve all orders |
| GET | `/api/orders/{id}` | Retrieve one order |
| GET | `/api/orders/search?customer_name=Anna` | Search by customer |
| PATCH | `/api/orders/{id}/status` | Update status or cancel |
| GET | `/api/orders/{id}/history` | Retrieve status history |
| GET | `/api/orders/status-transitions` | Retrieve permitted transitions |

### 3.1 Create a Repair Order

**Method:** POST  
**Endpoint:** `/api/orders`

All five required fields must be provided.

Successful response: HTTP 201 Created.

### 3.2 Retrieve All Repair Orders

**Method:** GET  
**Endpoint:** `/api/orders`

Returns all repair orders stored in the database.

Successful response: HTTP 200 OK.

### 3.3 Retrieve a Specific Repair Order

**Method:** GET  
**Endpoint:** `/api/orders/{id}`

Returns the requested order. A nonexistent order returns HTTP 404.

### 3.4 Search Repair Orders

**Method:** GET  
**Endpoint:** `/api/orders/search?customer_name=Anna`

Searches orders by customer name.

### 3.5 Update Repair Order Status

**Method:** PATCH  
**Endpoint:** `/api/orders/{id}/status`

Example request:

```json
{
  "status": "In Progress"
}
```

The backend validates both the status value and the permitted transition.

Cancellation is performed by setting the status to `Cancelled`.

### 3.6 Retrieve Status History

**Method:** GET  
**Endpoint:** `/api/orders/{id}/history`

Returns the order's status history, including old status, new status and timestamp.

### 3.7 Retrieve Permitted Status Transitions

**Method:** GET  
**Endpoint:** `/api/orders/status-transitions`

Returns the permitted next statuses for each current status.

### 3.8 Edit an Existing Repair Order

**Planned – Not Yet Available**

The planned editing functionality will allow changes to:
- customer_name
- customer_phone
- bicycle_type
- bicycle_brand
- problem_description

Implementation requires a database update function and coordination with the database developer.

The endpoint and request format must be agreed upon before implementation.

## 4. Repair Order Status Values

| Status | Description |
|---|---|
| Registered | Repair order has been created |
| Scheduled | Repair appointment has been arranged |
| In Progress | Bicycle repair has started |
| Waiting for Parts | Repair is waiting for required parts |
| Completed | Repair work has been completed |
| Cancelled | Repair order or appointment has been cancelled |

Initial status: `Registered`.

## 5. Business Workflow and Rules

### Permitted transitions

| Current status | Allowed next status |
|---|---|
| Registered | Scheduled, Cancelled |
| Scheduled | In Progress, Cancelled |
| In Progress | Waiting for Parts, Completed, Cancelled |
| Waiting for Parts | In Progress, Cancelled |
| Completed | None |
| Cancelled | None |

### Business rules

1. Only permitted status transitions are accepted.
2. Completed orders cannot return to earlier repair stages.
3. Cancelled orders cannot return to the normal repair workflow.
4. Repeating the current status does not create a duplicate history entry.
5. Successful status changes are recorded in status history.

These are the current proposed rules and must remain consistent with the agreed TO-BE BPMN and Lab 4 requirements.

## 6. Validation Rules

The backend validates all incoming information.

1. Customer name must not be empty.
2. Customer phone must not be empty.
3. Bicycle type must not be empty.
4. Bicycle brand must not be empty.
5. Problem description must not be empty.
6. Required fields must contain valid text.
7. Repair order IDs must be unique.
8. Status values must match the six permitted statuses.
9. Status transitions must follow the agreed workflow.
10. Invalid or incomplete requests must not be saved.
11. Nonexistent repair orders must not be updated.

## 7. Error Handling

| HTTP Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Repair order successfully created |
| 400 | Invalid request, validation error or forbidden transition |
| 404 | Requested repair order not found |
| 500 | Internal server error |

Validation errors return JSON containing `success: false`, a message and, where applicable, field-specific errors.

Forbidden transitions return HTTP 400.

Nonexistent orders return HTTP 404.

## 8. Database Requirements

The database developer is responsible for maintaining SQLite.

Current tables:
- `repair_orders`
- `status_history`

The database must support creating, retrieving, searching, updating statuses, recording history and retrieving history.

Editing order details is pending implementation of the required database operation.

## 9. Responsibilities of Each Developer

### 9.1 Frontend Developer – Augsta

Responsible for:
- Developing HTML pages.
- Designing CSS layouts.
- Implementing JavaScript functionality.
- Creating repair order registration forms.
- Displaying repair orders and details.
- Sending API requests.
- Displaying status history.
- Implementing editing and cancellation interfaces.
- Displaying success and error messages.
- Following permitted workflow transitions.

### 9.2 Backend Developer – Natnael

Responsible for:
- Developing the Flask application.
- Creating and maintaining API endpoints.
- Processing HTTP requests.
- Validating incoming information.
- Implementing business logic.
- Enforcing workflow transitions.
- Integrating status history.
- Handling errors.
- Testing backend functionality.
- Maintaining API documentation.

### 9.3 Database Developer – Soheib

Responsible for:
- Setting up SQLite.
- Designing the database schema.
- Creating tables and constraints.
- Implementing database operations.
- Ensuring data persistence.
- Providing database setup instructions.
- Coordinating database changes with the backend developer.

### 9.4 Shared Responsibilities

All three developers should follow the agreed API contract, coordinate changes, test integration and maintain the GitHub repository.

## 10. Integration Rules

1. All developers must use consistent field names.
2. The frontend must communicate through the documented API.
3. The backend handles validation and business logic.
4. The database handles persistent storage.
5. The frontend must handle API responses appropriately.
6. API or database changes must be discussed by all three developers.
7. The integrated application must be tested before submission.

## 11. Project Scope – MVP

### Implemented or verified

- Creating repair orders.
- Automatically generating repair order IDs.
- Saving repair orders.
- Retrieving all and individual orders.
- Searching by customer name.
- Updating repair statuses.
- Validating required information.
- Enforcing permitted status transitions.
- Cancelling orders through status updates.
- Maintaining status history.
- Persistent data storage.

### Pending

- Editing existing repair order details.
- Final verification of all laboratory requirements.
- Final integration and demonstration.

## 12. Version Control and Approval

This document proposes an update to API Contract Version 1.0.

**Version:** 1.1  
**Status:** Pending approval by all three developers.

**Team responsibilities:**
- Natnael – Backend Developer
- Augsta – Frontend Developer
- Soheib – Database Developer

Any changes must be discussed and agreed upon by the team.

**End of Document**

