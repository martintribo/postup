import { pgEnum, index, pgTable, serial, integer, text, timestamp, real, boolean, primaryKey, jsonb } from 'drizzle-orm/pg-core';

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
	googlePlaceId: text('google_place_id').unique(),
	parking: text('parking'),
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

export const joinMode = pgEnum('join_mode', ['open', 'ask']);
export const postStatus = pgEnum('post_status', ['live', 'ended', 'cancelled']);

export const post = pgTable('post', {
	id: serial('id').primaryKey(),
	name: text('name').notNull(),
	activity: text('activity').notNull(),
	location: text('location').notNull(),
	latitude: real('latitude').notNull(),
	longitude: real('longitude').notNull(),
	hours: integer('hours').notNull(),
	goals: text('goals'),
	neighborhood: text('neighborhood'),
	locality: text('locality'),
	district: text('district'),
	placeId: integer('place_id').references(() => place.id),
	sessionId: text('session_id'),
	userId: text('user_id').references(() => user.id),
	/** Optional project this postup is for (M3). */
	projectId: integer('project_id'),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	startTime: timestamp('start_time', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	/** Authoritative end time; backfilled from start_time + hours. */
	endsAt: timestamp('ends_at', { withTimezone: true, mode: 'date' }),
	joinMode: joinMode('join_mode').notNull().default('open'),
	capacity: integer('capacity'),
	status: postStatus('status').notNull().default('live'),
	note: text('note')
}, (t) => [index('post_status_ends_at_idx').on(t.status, t.endsAt)]);

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

export const agentToken = pgTable('agent_token', {
	id: text('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => user.id),
	agentSessionId: text('agent_session_id').notNull(),
	scope: text('scope').notNull().default('projects'),
	expiresAt: timestamp('expires_at', { withTimezone: true, mode: 'date' }).notNull(),
	revokedAt: timestamp('revoked_at', { withTimezone: true, mode: 'date' }),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
});

export const projectStatus = pgTable('project_status', {
	id: serial('id').primaryKey(),
	projectId: integer('project_id').notNull().references(() => project.id),
	title: text('title'),
	body: text('body').notNull(),
	occurredAt: timestamp('occurred_at', { withTimezone: true, mode: 'date' }).notNull(),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
});

export type ProjectStatus = typeof projectStatus.$inferSelect;

export const projectChange = pgTable('project_change', {
	id: serial('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => user.id),
	agentSessionId: text('agent_session_id').notNull(),
	action: text('action').notNull(),
	targetProjectId: integer('target_project_id').references(() => project.id),
	payload: jsonb('payload').notNull(),
	status: text('status').notNull().default('pending'),
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	reviewedAt: timestamp('reviewed_at', { withTimezone: true, mode: 'date' })
});

export type AgentToken = typeof agentToken.$inferSelect;
export type ProjectChange = typeof projectChange.$inferSelect;

export type Place = typeof place.$inferSelect;
export type PlaceReview = typeof placeReview.$inferSelect;
export type PlaceTag = typeof placeTag.$inferSelect;

/** M6: joining a postup. Open mode inserts 'approved' directly; ask mode starts 'pending'. */
export const joinStatus = pgEnum('join_status', ['pending', 'approved', 'declined', 'left', 'removed']);
export const joinRequest = pgTable(
	'join_request',
	{
		id: serial('id').primaryKey(),
		postId: integer('post_id').notNull().references(() => post.id),
		userId: text('user_id').notNull().references(() => user.id),
		reason: text('reason'),
		status: joinStatus('status').notNull().default('pending'),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
		decidedAt: timestamp('decided_at', { withTimezone: true, mode: 'date' })
	},
	(t) => [index('join_request_post_user_idx').on(t.postId, t.userId)]
);
export type JoinRequest = typeof joinRequest.$inferSelect;

/** M6: in-app activity (and the source for email/push later). */
export const notification = pgTable(
	'notification',
	{
		id: serial('id').primaryKey(),
		userId: text('user_id').notNull().references(() => user.id),
		type: text('type').notNull(), // join_request | joined | approved | declined | removed | left
		postId: integer('post_id').references(() => post.id),
		actorId: text('actor_id').references(() => user.id),
		body: text('body').notNull(),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
		readAt: timestamp('read_at', { withTimezone: true, mode: 'date' })
	},
	(t) => [index('notification_user_idx').on(t.userId, t.createdAt)]
);

/** M7: one group chat per postup (members = poster + approved joiners). */
export const message = pgTable(
	'message',
	{
		id: serial('id').primaryKey(),
		postId: integer('post_id').notNull().references(() => post.id),
		userId: text('user_id').notNull().references(() => user.id),
		body: text('body').notNull(),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
		deletedAt: timestamp('deleted_at', { withTimezone: true, mode: 'date' })
	},
	(t) => [index('message_post_idx').on(t.postId, t.id)]
);

export const chatRead = pgTable(
	'chat_read',
	{
		postId: integer('post_id').notNull().references(() => post.id),
		userId: text('user_id').notNull().references(() => user.id),
		lastReadId: integer('last_read_id').notNull().default(0)
	},
	(t) => [primaryKey({ columns: [t.postId, t.userId] })]
);

/** M8: reports (reviewed at /admin/reports) and blocks (two-way invisibility). */
export const report = pgTable('report', {
	id: serial('id').primaryKey(),
	reporterId: text('reporter_id').notNull().references(() => user.id),
	targetType: text('target_type').notNull(), // user | post | message | project
	targetId: text('target_id').notNull(),
	reason: text('reason').notNull(),
	details: text('details'),
	status: text('status').notNull().default('open'), // open | actioned | dismissed
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	resolvedAt: timestamp('resolved_at', { withTimezone: true, mode: 'date' })
});

export const block = pgTable(
	'block',
	{
		blockerId: text('blocker_id').notNull().references(() => user.id),
		blockedId: text('blocked_id').notNull().references(() => user.id),
		createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date())
	},
	(t) => [primaryKey({ columns: [t.blockerId, t.blockedId] })]
);

/** M10: native push tokens (APNs via FCM, or FCM). */
export const deviceToken = pgTable('device_token', {
	token: text('token').primaryKey(),
	userId: text('user_id').notNull().references(() => user.id),
	platform: text('platform').notNull(), // ios | android
	createdAt: timestamp('created_at', { withTimezone: true, mode: 'date' }).notNull().$defaultFn(() => new Date()),
	lastSeenAt: timestamp('last_seen_at', { withTimezone: true, mode: 'date' }).$defaultFn(() => new Date())
});
