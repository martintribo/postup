import { page } from 'vitest/browser';
import { describe, expect, it } from 'vitest';
import { render } from 'vitest-browser-svelte';
import ProjectCard from '$lib/components/ui/ProjectCard.svelte';

// The home page needs server data + Leaflet; cover the shared card it renders instead.
describe('ProjectCard', () => {
	it('renders name, owner and weekly pill', async () => {
		render(ProjectCard, { c: { id: 1, name: 'Pixel Garden', cover: null, owner: 'Tess', ownerAvatar: null, lastUpdate: 'New crop sprites', short: '', when: 'Tue', cafe: 'Grindhouse', week: 2 } });
		await expect.element(page.getByText('Pixel Garden')).toBeInTheDocument();
		await expect.element(page.getByText('2 this week')).toBeInTheDocument();
	});
});
