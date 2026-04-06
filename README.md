# 🍕 QuickBite API — Food Delivery Backend

![Node.js](https://img.shields.io/badge/Node.js-18+-green?logo=node.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue?logo=postgresql)
![Status](https://img.shields.io/badge/Status-Work--In--Progress-orange)

Welcome to the **QuickBite Food Delivery API**. This repository serves as a baseline for the **Performance Engineering & Scalability** assignment. The application provides an MVP backend for food ordering, restaurant listing, and user management.

---

## 🚀 Quick Start

Follow these steps to get the environment running in under 10 minutes:

### 1. Project Initialization
```bash
# Clone the repository
git clone https://github.com/kalviumcommunity/-Build-the-Backbone.git
cd -Build-the-Backbone

# Install dependencies
npm install
```

### 2. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env
```
*Note: Update `DATABASE_URL` in `.env` with your actual PostgreSQL connection string.*

### 3. Database Preparation
```bash
# Initialize schema (NO performance indexes included)
npm run migrate

# Seed with 30,000+ realistic Indian context records
npm run seed
```

### 4. Start the Application
```bash
# Start development server with hot-reload
npm run dev
```

---

## 📋 Prerequisites

- **Node.js**: v18.0.0 or higher
- **npm**: v8.0.0 or higher
- **PostgreSQL**: v14.0 or higher (Local or Managed)

---

## 🔧 Environment Variables

| Variable | Example | Required | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `postgres://user:pass@localhost:5432/quickbite` | Yes | PostgreSQL connection string |
| `JWT_SECRET` | `super-secret-key-1234` | Yes | Token signing secret |
| `PORT` | `3000` | No | Server listener port |
| `LOG_QUERIES` | `true` | No | Log every database query text & duration |
| `REDIS_URL` | `redis://localhost:6379` | No | Placeholder for caching optimization (Part B) |

---

## 📡 API Endpoints

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | No | System health and DB connectivity check |
| `POST` | `/api/auth/register` | No | Register a new customer |
| `POST` | `/api/auth/login` | No | Authenticate and get JWT token |
| `GET` | `/api/restaurants` | No | List restaurants by city with pagination |
| `GET` | `/api/restaurants/:id/menu` | No | Fetch menu with category nesting |
| `GET` | `/api/orders/history` | **Yes** | Fetch full history (Warning: Slow Response) |
| `POST` | `/api/orders` | **Yes** | Create new order (Warning: High Latency) |
| `GET` | `/api/orders/:id` | **Yes** | Get detailed order status |

---

## 🏗️ Project Structure

```text
.
├── migrations/
│   ├── 001_create_tables.sql   # Junior developer's original schema
│   └── 002_seed_data.sql       # High-volume Indian context data
├── src/
│   ├── controllers/            # Request handlers (with planted logic)
│   ├── db/                     # DB client wrapper & logging
│   ├── lib/                    # Shared services & simulations
│   ├── middleware/             # Auth & Error handling
│   ├── app.js                  # Express setup
│   └── server.js               # Entry point
├── artillery-baseline.yml      # Load testing configuration
└── users.csv                   # Test data for load scripts
```

---

## 🧪 Load Testing

Performance baselines are established using **Artillery.io**. To run the initial baseline test:

```bash
# Ensure the server is running first (npm run dev)
npm run test:load
```
This script simulates 100+ concurrent user journeys, including authentication and history retrieval. Use the resulting report to identify bottlenecks.

---

## 📊 Database Schema

- **`users`**: Contains customer profiles and credentials.
- **`restaurants`**: Catalog of 100 Indian restaurants across 5 major cities.
- **`categories`**: Menu organization (Starters, Breads, etc.) per restaurant.
- **`menu_items`**: Global catalog of thousands of Indian dishes.
- **`orders`**: Historical transaction records (5,000+ entries).
- **`order_items`**: Line item detail (30,000+ entries) mapped to orders.
- **`reviews`**: Customer feedback loop with ratings.

---

## 🛠️ Scripts

| Script | Command | Description |
| :--- | :--- | :--- |
| `start` | `node src/server.js` | Production start |
| `dev` | `nodemon src/server.js` | Development start with hot-reload |
| `migrate` | `psql $DATABASE_URL -f ...` | Wipe and recreate database schema |
| `seed` | `psql $DATABASE_URL -f ...` | Load high-volume seed data |
| `test:load` | `artillery run ...` | Execute baseline load profile test |

---

## ⚠️ Internal Notes
*The `order history` endpoint has been flagged by early testers for high latency. Investigation is required in the next sprint.*
