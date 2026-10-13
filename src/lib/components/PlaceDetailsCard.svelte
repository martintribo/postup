<script lang="ts">
	let { placeId }: { placeId: string } = $props();
</script>

<!-- Compact Place Details (UI Kit). Allowed beside a non-Google map (Maps SST 15.1).
     Weekly channel: orientation VERTICAL|HORIZONTAL as the JS property (lowercase is rejected).
     VERTICAL in the 340px sidebar so gmp-place-media is not dropped; attribution stays in content-config. -->
<gmp-place-details-compact orientation="VERTICAL">
	<gmp-place-details-place-request place={placeId}></gmp-place-details-place-request>
	<gmp-place-content-config>
		<gmp-place-media lightbox-preferred preferred-size="MEDIUM"></gmp-place-media>
		<gmp-place-rating></gmp-place-rating>
		<gmp-place-type></gmp-place-type>
		<gmp-place-price></gmp-place-price>
		<gmp-place-accessible-entrance-icon></gmp-place-accessible-entrance-icon>
		<gmp-place-open-now-status></gmp-place-open-now-status>
		<gmp-place-attribution
			light-scheme-color="gray"
			dark-scheme-color="white"
		></gmp-place-attribution>
	</gmp-place-content-config>
</gmp-place-details-compact>

<style>
	gmp-place-details-compact {
		display: block;
		width: 100%;
		max-width: 100%;
	}
</style>
