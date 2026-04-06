# 🍔 QuickBite: Performance Lab Boilerplate 🚀

Welcome to the **QuickBite Performance Engineering Challenge**! This repository contains a production-ready (functional) food delivery API built with Node.js and PostgreSQL.

While the app "works," it has been architected by a "junior developer" who prioritized features over performance. Your mission is to profile, identify bottlenecks, and optimize the API to handle production-scale traffic.

---

## 🛠️ Tech Stack

- **Runtime**: Node.js v16+
- **Framework**: Express.js
- **Database**: PostgreSQL (Raw `pg` driver)
- **Auth**: JWT & Bcrypt (12 rounds)
- **Testing**: Artillery (Load Profiling)

---

## 🏗️ Getting Started

### 1. Prerequisites
- **PostgreSQL** installed and running.
- **Node.js** (LTS recommended).

### 2. Environment Setup
Copy the example environment file and update your database credentials.

```bash
cp .env.example .env
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Database Setup
Create a database named `quickbite` and run the migrations.

```bash
# Create tables (WITHOUT Indexes - intentional!)
npm run migrate

# Seed with 30k+ records
npm run seed
```

### 5. Launch the Server
```bash
# Development mode with hot-reloading
npm run dev
```

---

## 🧪 Profiling the API

The application is slow. **Deliberately slow.** 🐌

### Baseline Load Test
Run the Artillery script to see how the system performs under moderate load:

```bash
npm run test:load
```

### 🔍 Discovery Checklist
Students should investigate the following:
1. **N+1 Query Patterns**: Check the logs when fetching order history. Why are there so many DB calls? 🕵️‍♂️
2. **Missing Indexes**: Run `EXPLAIN ANALYZE` on common filter queries like searching restaurants by city. 📈
3. **Blocking Synchronous Tasks**: Why does `POST /orders` take nearly a second even for a single item? ⏳
4. **Foreign Key Performance**: What happens to join performance as the `order_items` table grows?

---

## 🎯 Optimization Tasks
- [ ] Fix the N+1 in `src/controllers/order.controller.js`.
- [ ] Fix the N+1 in `src/controllers/restaurant.controller.js`.
- [ ] Implement missing indexes for all foreign key columns.
- [ ] Offload the `emailService` call to a background worker or use a `setImmediate`/`Promise` non-blocking pattern.

---

## 📜 API Documentation

### Auth
- `POST /api/auth/register`: Create a new user.
- `POST /api/auth/login`: Get a JWT token.

### Restaurants
- `GET /api/restaurants`: List restaurants (supports `city`, `limit`, `offset`).
- `GET /api/restaurants/:id/menu`: Get menu items for a restaurant.

### Orders
- `GET /api/orders/history`: (Protected) Fetch user's full order history.
- `POST /api/orders`: (Protected) Create a new food order.
- `GET /api/orders/:id`: (Protected) Details for a single order.

---

## ⚠️ Disclaimer
This code is intentionally suboptimal for educational purposes. Do not use this pattern in production (unless you want to be paged at 3 AM)! 😴

Happy Profiling! 🚀✨
