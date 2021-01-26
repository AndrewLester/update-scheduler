<script lang="ts">
import Button, { Group, Icon } from '@smui/button/bare';
import '@smui/button/bare.css';
import { createEventDispatcher } from 'svelte';
import type { Update } from '../api/types';
import { updates } from '../stores';

export let update: Update;
export let selected: boolean;

const dispatch = createEventDispatcher();

function deleteUpdate() {
    dispatch('delete');
    // TODO launch confirm dialog
    updates.delete(update, 'id');
}

</script>

<div class="card" class:selected>
    <p>{update.body}</p>
    <Group variant={'outlined'} style="width: 100%">
        <Button on:click={() => dispatch('edit')}><Icon class="material-icons">edit</Icon></Button>
        <Button on:click={deleteUpdate}><Icon class="material-icons">delete</Icon></Button>
    </Group>
</div>

<style>
.card {
    display: flex;
    flex-flow: column nowrap;
    align-items: stretch;
    height: 100px;
    width: 150px;
    max-height: 100%;
    border-radius: 5px;
    background: hotpink;
}

.card.selected {
    outline: 2px solid lightskyblue;
}
</style>