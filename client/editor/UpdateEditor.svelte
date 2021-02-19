<script lang="ts">
import Button, { Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import { getContext } from 'svelte';
import type { Update } from '../api/types';
import { getNewUpdate, isScheduled } from '../api/types';
import * as notification from '../notifications/notifier';
import { updates } from '../stores';
import TextEditor from '../utility/components/TextEditor.svelte';
import UpdateTimePicker from './UpdateTimePicker.svelte';

export let update: Update;

const isMobile = getContext<() => boolean>('mobile');

let editor: TextEditor | undefined;
let timePicker: UpdateTimePicker | undefined;
let updateMinusJob: Update;
const getUpdateBody = () => update.body;
let body = '';
$: id = update.id;
$: if (id && editor) editor.setContent(getUpdateBody());

$: if (update.job === null) {
    update.job = { id: '' };
}
$: job = update.job!;
$: scheduled = isScheduled(update);
$: {
    let { job, ...partialUpdate } = update;
    updateMinusJob = { ...partialUpdate, job: null };
}

async function save(updateData: Update) {
    let returnedData: Update | undefined;
    if (updateData.id === -1) {
        returnedData = await updates.create({ ...updateData, body });
    } else {
        // No need to await this because it can happen while the editor page is clearing
        // Since it just syncs the job id that was created
        returnedData = await updates.update({ ...updateData, body }, 'id').then(() => updates.sync('id', update.id));
    }

    if (isMobile()) {
        notification.info('Saved update', 2000);
    }

    // There was an error
    if (!returnedData) return;

    resetUpdate();
}

function handleNewUpdate() {
    if (update.id >= 0) {
        save(scheduled ? update : updateMinusJob);
        return;
    }
    
    resetUpdate();
}

async function resetUpdate() {
    update = getNewUpdate();
    editor?.clear();
    timePicker?.clear();
}
</script>

<div class="editor">
    <div class="button-row" style="margin-bottom: 5px; gap: 15px;">
        <Button class="new-button" on:click={handleNewUpdate} variant="outlined"><Label>New Update</Label></Button>
        <h3>Create and Schedule an Update</h3>
    </div>
    <TextEditor placeholder={'Write update'} bind:content={body} bind:this={editor} />
    <div class="button-row">
        {#key id}
            <UpdateTimePicker {job} bind:this={timePicker} />
        {/key}
        <div class="save-buttons">
            <Button on:click={() => save(scheduled ? update : updateMinusJob)} variant="outlined"><Label>Save</Label></Button>
            {#if !scheduled }
                <Button on:click={() => save(update)} variant="raised"><Label>Save and Schedule</Label></Button>
            {:else}
                <Button on:click={() => update = getNewUpdate()} variant="outlined"><Label>Discard Edit</Label></Button>
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
    flex-flow: row wrap;
    align-items: center;
}

.save-buttons {
    margin-left: auto;
}
</style>
