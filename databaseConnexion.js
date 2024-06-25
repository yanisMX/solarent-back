import pg from "pg";
import "dotenv/config";

const { PGHOST, PGDATABASE, PGUSER, PGPASSWORD } = process.env;

const pool = new pg.Pool({
    user: PGUSER,
    host: PGHOST,
    database: PGDATABASE,
    password: PGPASSWORD,
    port: 5432,
    ssl: {
        rejectUnauthorized: false,
    },
});

export async function executeCommand(command) {
    const client = await pool.connect();
    try {
        const result = await command(client);
        return result;
    } finally {
        client.release();
    }
}