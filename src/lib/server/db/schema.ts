import { pgTable, serial, integer, text, timestamp, real, boolean, primaryKey } from 'drizzle-orm/pg-core';

export const user = pgTable('user', {
	id: text('id').primaryKey(),
	age: integer('age'),
	username: text('username').notNull().unique(),
	/** Null for accounts created through Apple/Google. */
	passwordHash: text('password_hash'),
	displayName: text('display_name'),
	avatarUrl: text('avatar_url'),
	email: text('email'),
	bio: text('bio'),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).$defaultFn(() => new Date())
});

/** One row per linked Apple/Google identity. */
export const oauthAccount = pgTable(
	'oauth_account',
	{
		provider: text('provider').notNull(),
		providerUserId: text('provider_user_id').notNull(),
		userId: text('user_id')
			.notNull()
			.references(() => user.id),
		email: text('email'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).$defaultFn(() => new Date())
	},
	(t) => [primaryKey({ columns: [t.provider, t.providerUserId] })]
);

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
	activity: text('activity').notNull(),
	location: text('location').notNull(),
	latitude: real('latitude').notNull(),
	longitude: real('longitude').notNull(),
	hours: integer('hours').notNull(),
	neighborhood: text('neighborhood'),
	locality: text('locality'),
	district: text('district'),
	sessionId: text('session_id'),
	userId: text('user_id').references(() => user.id),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	startTime: timestamp('start_time', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
});

export type Session = typeof session.$inferSelect;

export type User = typeof user.$inferSelect;

export type Post = typeof post.$inferSelect;

export const project = pgTable('project', {
	id: serial('id').primaryKey(),
	name: text('name').notNull(),
	type: text('type').notNull().default('software'),
	shortDescription: text('short_description').notNull(),
	description: text('description').notNull(),
	active: boolean('active').notNull().default(true),
	/** Hidden from public lists (test/seed junk). */
	hidden: boolean('hidden').notNull().default(false),
	sessionId: text('session_id'),
	userId: text('user_id').references(() => user.id),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	lastPostUpAt: timestamp('last_post_up_at', { withTimezone: true, mode: 'date' })
});

export type Project = typeof project.$inferSelect;
