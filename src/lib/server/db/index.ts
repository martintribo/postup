import { drizzle as drizzleNeon } from 'drizzle-orm/neon-http';
import { drizzle as drizzlePg } from 'drizzle-orm/postgres-js';
import { neon } from '@neondatabase/serverless';
import postgres from 'postgres';
import * as schema from './schema';
import { env } from '$env/dynamic/private';

if (!env.DATABASE_URL) throw new Error('DATABASE_URL is not set');

const url = env.DATABASE_URL;

/** neon-http talks to Neon’s HTTP API, not local Postgres TCP. */
function isNeonUrl(u: string) {
	return /neon\.tech|neon\.build/i.test(u) || /^https:/i.test(u);
}

export const db = isNeonUrl(url)
	? drizzleNeon(neon(url), { schema })
	: drizzlePg(postgres(url, { max: 4 }), { schema });
