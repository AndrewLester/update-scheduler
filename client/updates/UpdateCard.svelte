<script lang="ts">
import Button, { Group, Icon, Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import moment from 'moment';
import { createEventDispatcher } from 'svelte';
import type { Update } from '../api/types';
import { updates } from '../stores';

export let update: Update;
export let selected: boolean;

$: scheduled = (update.job?.scheduled_for || update.job?.scheduled_in);
let scheduledText = '';
$: if (scheduled) {
    if (update.job?.scheduled_in) {
        scheduledText = update.job.scheduled_in;
        console.log(update);
    } else if (update.job?.scheduled_for) {
        scheduledText = moment.duration(moment(update.job.scheduled_for).diff(moment())).humanize(true);
    }
}

const dispatch = createEventDispatcher();

function deleteUpdate() {
    dispatch('delete');
    // TODO launch confirm dialog
    updates.delete(update, 'id');
}

function cancelUpdate() {
    update.job = null;
    updates.update(update, 'id');
}

</script>

<div class="card" class:selected>
    <p>
        <Icon class="material-icons" style="float: left; margin-right: 5px; font-size: 23px">chat</Icon>
        {update.body}
    </p>
    {#if scheduled}
        <p style="display: flex; align-items: center;">
            <Icon class="material-icons" style="float: left; margin-right: 5px; font-size: 23px">schedule</Icon>
            {'Posts ' + scheduledText}
        </p>
    {/if}
    <Group style="width: 100%; margin-top: auto">
        <Button on:click={() => dispatch('edit')} disabled={selected}><Icon class="material-icons">edit</Icon><Label>Edit</Label></Button>
        {#if scheduled }
            <Button on:click={cancelUpdate}><Icon class="material-icons">cancel</Icon><Label>Cancel</Label></Button>
        {:else}    
            <Button on:click={deleteUpdate}><Icon class="material-icons">delete</Icon><Label>Delete</Label></Button>
        {/if}
    </Group>
</div>

<style>
.card {
    display: flex;
    flex-flow: column nowrap;
    align-items: stretch;
    height: 100px;
    width: 175px;
    max-height: 100%;
    border-radius: 5px;
    background: white;
}

p {
    max-height: 100%;
    padding: 5px 10px;
    overflow-wrap: break-word;
    vertical-align: middle;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card.selected {
    box-shadow: 0px 0px 0px 2px lightskyblue;
}
</style>