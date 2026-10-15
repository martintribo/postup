/** Share a PostUp link: native share sheet where available, else copy to clipboard. Returns what happened. */
export async function shareLink(path: string, text: string): Promise<'shared' | 'copied' | 'none'> {
	const url = new URL(path, location.origin).toString();
	try {
		if (navigator.share) {
			await navigator.share({ url, text });
			return 'shared';
		}
		await navigator.clipboard.writeText(url);
		return 'copied';
	} catch {
		return 'none';
	}
}
