import { pgTable, serial, integer, text, timestamp, real, boolean, jsonb } from 'drizzle-orm/pg-core';

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

export const place = pgTable('place', {
	id: serial('id').primaryKey(),
	name: text('name').notNull(),
	address: text('address').notNull(),
	latitude: real('latitude').notNull(),
	longitude: real('longitude').notNull(),
	mapboxId: text('mapbox_id'),
	category: text('category'),
	openHours: jsonb('open_hours'),
	website: text('website'),
	phone: text('phone'),
	googlePlaceId: text('google_place_id'),
	photoRef: text('photo_ref'),
	sessionId: text('session_id'),
	createdBy: text('created_by').references(() => user.id),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
});

export const placeReview = pgTable('place_review', {
	id: serial('id').primaryKey(),
	placeId: integer('place_id').notNull().references(() => place.id),
	userId: text('user_id').references(() => user.id),
	sessionId: text('session_id'),
	rating: integer('rating').notNull(),
	text: text('text'),
	wifiRating: integer('wifi_rating'),
	noiseLevel: text('noise_level'),
	hasOutlets: boolean('has_outlets'),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
});

export const placeTag = pgTable('place_tag', {
	id: serial('id').primaryKey(),
	placeId: integer('place_id').notNull().references(() => place.id),
	tag: text('tag').notNull(),
	votes: integer('votes').notNull().default(1)
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
	placeId: integer('place_id').references(() => place.id),
	sessionId: text('session_id'),
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
	sessionId: text('session_id'),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	lastPostUpAt: timestamp('last_post_up_at', { withTimezone: true, mode: 'date' })
});

export type Project = typeof project.$inferSelect;

export type Place = typeof place.$inferSelect;
export type PlaceReview = typeof placeReview.$inferSelect;
export type PlaceTag = typeof placeTag.$inferSelect;
