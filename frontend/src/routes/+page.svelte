<script lang="ts">
	let images: FileList | null = null;
	let processed_images: string[] = [];

	function handleFileChange(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		images = input.files ?? null;
	}

	const upload = async () => {
		if (!images || images.length === 0) return;

		const formData = new FormData();

		// append all images under the same field name (FastAPI expects this)
		for (let i = 0; i < images.length; i++) {
			formData.append("files", images[i]);   
		}

		const res = await fetch("http://localhost:8000/images", {
			method: "POST",
			body: formData
		});

		if (!res.ok) {
			console.error("processing failed");
			return;
		}

	};
</script>

<!-- allow multiple file selection -->
<input type="file" multiple on:change={handleFileChange} />
<button on:click={upload}>Process</button>

{#if processed_images.length > 0}
	<h3>Processed Images:</h3>
	{#each processed_images as img}
		<img src={img} alt="Processed" />
	{/each}
{/if}
