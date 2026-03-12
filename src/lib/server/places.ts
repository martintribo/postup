export interface OpenPeriod {
	open: { day: number; time: string };
	close?: { day: number; time: string };
}

function parseMinutes(time: string): number {
	return parseInt(time.slice(0, 2)) * 60 + parseInt(time.slice(2));
}

export function isCurrentlyOpen(periods: OpenPeriod[], tzOffset?: number): { isOpen: boolean; closesAt: string | null; opensAt: string | null } {
	if (!periods || periods.length === 0) {
		return { isOpen: false, closesAt: null, opensAt: null };
	}

	// A single period with open 0000 and no close = 24/7
	// Also: any period with no close field = open all day from that time
	const has24x7 = periods.some(p => !p.close && p.open.time === '0000');
	if (has24x7) {
		return { isOpen: true, closesAt: null, opensAt: null };
	}

	const now = new Date();
	let localNow: Date;
	if (tzOffset !== undefined && !isNaN(tzOffset)) {
		const utcMs = now.getTime() + now.getTimezoneOffset() * 60000;
		localNow = new Date(utcMs - tzOffset * 60000);
	} else {
		localNow = now;
	}
	const day = localNow.getDay();
	const nowMinutes = localNow.getHours() * 60 + localNow.getMinutes();
	const yesterday = (day + 6) % 7;

	// Check if currently within any period (including overnight spans)
	for (const period of periods) {
		// No close = open all day from open time
		if (!period.close) {
			if (period.open.day === day && nowMinutes >= parseMinutes(period.open.time)) {
				return { isOpen: true, closesAt: null, opensAt: null };
			}
			continue;
		}

		const openMinutes = parseMinutes(period.open.time);
		const closeMinutes = parseMinutes(period.close.time);

		// 0000-0000 = open 24 hours that day
		if (openMinutes === 0 && closeMinutes === 0) {
			if (period.open.day === day) {
				return { isOpen: true, closesAt: null, opensAt: null };
			}
			continue;
		}

		const isOvernight = closeMinutes <= openMinutes;

		if (isOvernight) {
			if (period.open.day === day && nowMinutes >= openMinutes) {
				return { isOpen: true, closesAt: formatTime(period.close.time), opensAt: null };
			}
			if (period.open.day === yesterday && nowMinutes < closeMinutes) {
				return { isOpen: true, closesAt: formatTime(period.close.time), opensAt: null };
			}
		} else {
			if (period.open.day === day && nowMinutes >= openMinutes && nowMinutes < closeMinutes) {
				return { isOpen: true, closesAt: formatTime(period.close.time), opensAt: null };
			}
		}
	}

	// Not open — find when it most recently closed
	let closedAt: string | null = null;
	for (const period of periods) {
		if (!period.close) continue;

		const closeMinutes = parseMinutes(period.close.time);
		const openMinutes = parseMinutes(period.open.time);

		if (openMinutes === 0 && closeMinutes === 0) continue;

		const isOvernight = closeMinutes <= openMinutes;

		if (isOvernight) {
			if (period.open.day === yesterday && closeMinutes <= nowMinutes) {
				closedAt = formatTime(period.close.time);
			}
		} else {
			if (period.open.day === day && closeMinutes <= nowMinutes) {
				closedAt = formatTime(period.close.time);
			}
		}
	}

	// Find next open time
	for (let offset = 0; offset < 7; offset++) {
		const checkDay = (day + offset) % 7;
		for (const period of periods) {
			if (period.open.day === checkDay) {
				const openMinutes = parseMinutes(period.open.time);
				if (offset === 0 && openMinutes <= nowMinutes) continue;
				const dayLabel = offset === 0 ? '' : offset === 1 ? 'tomorrow ' : dayName(checkDay) + ' ';
				return {
					isOpen: false,
					closesAt: closedAt,
					opensAt: `${dayLabel}${formatTime(period.open.time)}`
				};
			}
		}
	}

	return { isOpen: false, closesAt: closedAt, opensAt: null };
}

function formatTime(time: string): string {
	const h = parseInt(time.slice(0, 2));
	const m = time.slice(2);
	const suffix = h >= 12 ? 'PM' : 'AM';
	const h12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
	return m === '00' ? `${h12} ${suffix}` : `${h12}:${m} ${suffix}`;
}

function dayName(day: number): string {
	return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][day];
}
