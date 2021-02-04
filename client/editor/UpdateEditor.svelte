<script lang="ts">
import Button, { Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import Textfield from '@smui/textfield/bare';
import '@smui/textfield/bare.css';
import type { Update } from '../api/types';
import { getNewUpdate } from '../App.svelte';
import { updates } from '../stores';
import TextEditor from '../utility/components/TextEditor.svelte';
import UpdateTimePicker from './UpdateTimePicker.svelte';

export let update: Update;

$: id = update.id;
let value: string = '';
let editor: TextEditor | undefined;
let updateMinusJob: Update;
$: scheduled = update.job?.id !== '';
$: {
    let { job, ...partialUpdate } = update;
    updateMinusJob = { ...partialUpdate, job: null };
}
const getUpdateBody = () => update.body;
$: if (editor && id) {
    editor.setContent(getUpdateBody());
}

async function save(updateData: Update) {
    if (updateData.id === -1) {
        const newUpdate = await updates.create(updateData);
        // Error creating update
        if (editor) editor.clear();
        if (!newUpdate) return;

        update = newUpdate;
    } else {
        updates.update(updateData, 'id');
    }

    if (editor) editor.clear();
    update = getNewUpdate();
}
</script>



<div class="editor">
    <div class="button-row" style="margin-bottom: 5px; gap: 15px;">
        <Button class="new-button" on:click={() => save(scheduled ? update : updateMinusJob)} variant="outlined"><Label>New Update</Label></Button>
        <h3>Create and Schedule an Update</h3>
    </div>
    <!-- <Textfield fullwidth textarea bind:value={update.body} label="Write update" input$aria-controls="helper-text-fullwidth-textarea" input$aria-describedby="helper-text-fullwidth-textarea" /> -->
    <TextEditor placeholder={'Write update'} bind:content={update.body} bind:this={editor} />
    <div class="button-row">
        <UpdateTimePicker bind:update={update} />
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
