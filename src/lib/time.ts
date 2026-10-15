/** "4pm", "3:45pm" in the viewer's zone. */
export function clock(d: Date | string): string {
	const x = typeof d === 'string' ? new Date(d) : d;
	return x.toLocaleTimeString('en-US', { hour: 'numeric', minute: x.getMinutes() ? '2-digit' : undefined }).replace(' ', '').toLowerCase();
}
