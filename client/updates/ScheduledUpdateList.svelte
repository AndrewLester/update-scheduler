<script lang="ts">
import type { Update } from "../api/types";

import CardList from "../layouts/CardList.svelte";
import UpdateCard from "./UpdateCard.svelte";

export let scheduledUpdates: Update[];

</script>

<CardList header={'Scheduled Updates'} horizontal items={scheduledUpdates} let:item>
    <UpdateCard update={item} />
</CardList>

<style>

</style>