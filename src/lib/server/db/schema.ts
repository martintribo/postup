import { pgTable, serial, integer, text, timestamp, real } from 'drizzle-orm/pg-core';

export const user = pgTable('user', {
	id: text('id').primaryKey(),
	age: integer('age'),
	username: text('username').notNull().unique(),
	passwordHash: text('password_hash').notNull()
});

export const session = pgTable('session', {
	id: text('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => user.id),
	expiresAt: timestamp('expires_at', { withTimezone: true, mode: 'date' }).notNull()
});

export const post = pgTable('post', {
	id: serial('id').primaryKey(),
	name: text('name').notNull(),
	location: text('location').notNull(),
	latitude: real('latitude').notNull(),
	longitude: real('longitude').notNull(),
	hours: integer('hours').notNull(),
	neighborhood: text('neighborhood'),
	locality: text('locality'),
	district: text('district'),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	startTime: timestamp('start_time', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
});

export type Session = typeof session.$inferSelect;

export type User = typeof user.$inferSelect;

export type Post = typeof post.$inferSelect;
