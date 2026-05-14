const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

pool.on('connect', () => {
  console.log('PostgreSQL connected');
});

module.exports = {
  /**
   * Execute a SQL query.
   * Logs duration and query text if LOG_QUERIES is set.
   */
  async query(text, params) {
    const start = Date.now();
    try {
      if (global.currentReq) {
        global.currentReq._queryCount++
      }

      const res = await pool.query(text, params);
      const duration = Date.now() - start;

      if (process.env.LOG_QUERIES === 'true') {
        console.log('Executing query:', text);
        console.log('[DB Query]', {
          text: text.replace(/\s+/g, ' ').trim(),
          duration: `${duration}ms`,
          rows: res.rowCount,
        });
      }

      return res;
    } catch (err) {
      console.error('[DB Error]', err.stack);
      throw err;
    }
  },

  // Expose pool for transactions or advanced usage
  pool
};
