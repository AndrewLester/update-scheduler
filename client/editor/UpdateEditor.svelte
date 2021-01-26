<script lang="ts">
import Button, { Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import Textfield from '@smui/textfield/bare';
import '@smui/textfield/bare.css';
import type { Update } from '../api/types';
import { getNewUpdate } from '../App.svelte';
import { updates } from '../stores';

export let update: Update;

let value: string = '';
let updateMinusJob: Update;
$: scheduled = update.job;
$: {
    let { job, ...partialUpdate } = update;
    updateMinusJob = { ...partialUpdate, job: null };
}

async function save(updateData: Update) {
    if (updateData.id === -1) {
        const newUpdate = await updates.create(updateData);
        // Error creating update
        if (!newUpdate) return;

        update = newUpdate;
    } else {
        updates.update(updateData, 'id');
    }

    update = getNewUpdate();
}

</script>

<div class="editor">
    <h3>Create and Schedule an Update</h3>
    <Textfield fullwidth textarea bind:value={update.body} label="Write update" input$aria-controls="helper-text-fullwidth-textarea" input$aria-describedby="helper-text-fullwidth-textarea" />
    <Button on:click={() => save(scheduled ? update : updateMinusJob)} variant="outlined"><Label>Save</Label></Button>
    {#if !update.job }
        <Button on:click={() => save(update)} variant="raised"><Label>Save and Schedule</Label></Button>
    {/if}
</div>


<style>
h3 {
    margin-top: 0px;
}

.editor {
    border-radius: 15px;
    background: white;
    height: 100%;
    width: 100%;
    padding: 20px 40px;
    overflow-y: auto;
    margin-bottom: 10px;
}
</style>