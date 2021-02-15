<script lang="ts">
import Button, { Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import { tick } from 'svelte';
import type { Update } from '../api/types';
import { isScheduled } from '../api/types';
import { getNewUpdate } from '../App.svelte';
import { updates } from '../stores';
import TextEditor from '../utility/components/TextEditor.svelte';
import UpdateTimePicker from './UpdateTimePicker.svelte';

export let update: Update;

let editor: TextEditor | undefined;
let timePicker: UpdateTimePicker | undefined;
let updateMinusJob: Update;
$: scheduled = isScheduled(update);
$: {
    let { job, ...partialUpdate } = update;
    updateMinusJob = { ...partialUpdate, job: null };
}

const getUpdateBody = () => update.body;
$: idChanged = update.id;
$: if (editor && timePicker && idChanged) {
    editor.setContent(getUpdateBody());
    timePicker.clear();
}

async function save(updateData: Update) {
    if (updateData.id === -1) {
        updates.create(updateData);
    } else {
        // No need to await this because it can happen while the editor page is clearing
        // Since it just syncs the job id that was created
        updates.update(updateData, 'id').then(() => updates.sync(updateData, 'id'));
    }

    await resetUpdate();
}

function handleNewUpdate() {
    if (update.id >= 0) {
        save(scheduled ? update : updateMinusJob);
        return;
    }
    
    resetUpdate();
}

async function resetUpdate() {
    if (editor && timePicker) {
        editor.clear();
        timePicker.clear();
    }

    // Wait for editor to clear
    await tick();

    update = getNewUpdate();
}
</script>

<div class="editor">
    <div class="button-row" style="margin-bottom: 5px; gap: 15px;">
        <Button class="new-button" on:click={handleNewUpdate} variant="outlined"><Label>New Update</Label></Button>
        <h3>Create and Schedule an Update</h3>
    </div>
    <TextEditor placeholder={'Write update'} bind:content={update.body} bind:this={editor} />
    <div class="button-row">
        <UpdateTimePicker bind:update={update} bind:this={timePicker} />
        <div class="save-buttons">
            <Button on:click={() => save(scheduled ? update : updateMinusJob)} variant="outlined"><Label>Save</Label></Button>
            {#if !scheduled }
                <Button on:click={() => save(update)} variant="raised"><Label>Save and Schedule</Label></Button>
            {/if}
        </div>
    </div>
</div>


<style>
h3 {
    margin: 0px;
}

.editor {
    border-radius: 15px;
    background: white;
    height: 100%;
    width: 100%;
    padding: 20px 40px;
    padding-bottom: 0px;
    overflow-y: auto;
    margin-bottom: 10px;
}

.button-row {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}

.save-buttons {
    margin-left: auto;
}
</style>
