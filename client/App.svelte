<script lang="ts">
import { onDestroy } from 'svelte';

let text = 0;
const scheduler = setInterval(() => text = text === 0 ? 1 : 0, 1000);

onDestroy(() => clearInterval(scheduler));
</script>

<main>
    <h1>Testing {text}</h1>
</main>

<style>

</style>