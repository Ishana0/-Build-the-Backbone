const db = require('../db');

/**
 * Get List of Restaurants with filters.
 * 
 * [PLANTED PERFORMANCE PROBLEM 3]
 * Missing indexes on WHERE and JOIN columns in the database.
 * This query will scan the full table even with a simple city filter.
 */
const getRestaurants = async (req, res) => {
    const { city, limit = 20, offset = 0 } = req.query;

    let queryStr = 'SELECT * FROM restaurants';
    const params = [];

    if (city) {
        queryStr += ' WHERE city = $1';
        params.push(city);
        queryStr += ` LIMIT $2 OFFSET $3`;
        params.push(limit, offset);
    } else {
        queryStr += ` LIMIT $1 OFFSET $2`;
        params.push(limit, offset);
    }

    const result = await db.query(queryStr, params);

    res.json({
        total: result.rowCount,
        restaurants: result.rows
    });
};

/**
 * Get Restaurant Menu items with category details.
 * 
 * [PLANTED PERFORMANCE PROBLEM 4]
 * N+1 for category details inside a loop.
 */
const getMenu = async (req, res) => {
    const { id } = req.params;

    console.log(`[Restaurant Controller] Fetching menu for Restaurant #${id}`);

    // Query 1: Get menu items
    const menuItemsResult = await db.query(
        'SELECT * FROM menu_items WHERE restaurant_id = $1 AND available = TRUE',
        [id]
    );
    const menuItems = menuItemsResult.rows;

    const populatedMenu = [];

    // // Attach category details to each item (N+1 query pattern)
    // For each menu item, perform a separate query to fetch its category name.
    for (const item of menuItems) {
        const categoryResult = await db.query(
            'SELECT * FROM categories WHERE id = $1',
            [item.category_id]
        );
        
        populatedMenu.push({
            ...item,
            category: categoryResult.rows[0] ? categoryResult.rows[0].name : 'Uncategorized'
        });
    }

    res.json({
        restaurant_id: id,
        menu: populatedMenu
    });
};

const getHealth = async (req, res) => {
    try {
        await db.query('SELECT 1');
        res.json({ status: 'UP', database: 'connected' });
    } catch (err) {
        res.status(503).json({ status: 'DOWN', database: 'disconnected' });
    }
};

module.exports = {
    getRestaurants,
    getMenu,
    getHealth
};
