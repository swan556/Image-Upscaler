<script lang="ts">
	let image: File | null = null;
	let processed_image: string | null = null;

	function handleFileChange(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		image = input.files?.[0] ?? null;
	}

	const upload = async () => {
		if (!image) return;

		const formData = new FormData();
		formData.append("file", image);

		const res = await fetch("http://localhost:8000/process", {
			method: "POST",
			body: formData
		});

		if (!res.ok) {
			console.error("processing failed");
			return;
		}

		const blob = await res.blob();
		processed_image = URL.createObjectURL(blob);
	};
</script>

<input type="file" on:change={handleFileChange} />
<button on:click={upload}>Process</button>

{#if processed_image}
	<h3>Processed Image:</h3>
	<img src={processed_image} alt="Processed" />
{/if}
