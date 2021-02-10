<script lang="ts">
import Button, { Group, Icon, Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import Dialog from '@smui/dialog/Dialog.svelte';
import {Title, Content, Actions, InitialFocus} from '@smui/dialog/bare';
import '@smui/dialog/bare.css';
import moment from 'moment';
import { createEventDispatcher } from 'svelte';
import type { Update } from '../api/types';
import { schoologyTimeToMoment } from '../api/types';
import { isScheduled } from '../api/types';
import { realms, time, updates } from '../stores';
import { sleep } from '../utility/async';
import tippy from '../utility/tippy';

export let update: Update;
export let selected: boolean;

let confirmDeleteDialog: Dialog;
let posted = false;
$: scheduled = isScheduled(update);
$: realmName = $realms.find((realm) => realm.id === update.realm_id)?.name;
let scheduledText = '';
const resetJob = () => update.job = null;
$: if (scheduled) {
    if (update.job?.scheduled_in) {
        scheduledText = moment.duration(update.job.scheduled_in).humanize(true);
    } else if (update.job?.scheduled_for) {
        const duration = moment.duration(schoologyTimeToMoment(update.job.scheduled_for).diff($time));
        if (duration.asMilliseconds() <= 0 && !posted) {
            posted = true;
            resetJob();
            sleep(1500).then(() => updates.reset());
        } else {
            scheduledText = duration.humanize(true);
        }
    }
}

$: realmNameTippyProps = { 
    content: realmName,
    placement: 'right',
    arrow: true,
    duration: [100, 100],
    animation: 'shift-away-subtle',
    touch: ['hold', 450],
    trigger: 'mouseenter'
}

const dispatch = createEventDispatcher();

function deleteUpdate(confirm: boolean) {
    if (confirm) {
        confirmDeleteDialog.open();
        return;
    }

    dispatch('delete');
    
    updates.delete(update, 'id');
}

function cancelUpdate() {
    update.job = null;
    updates.update(update, 'id');
}

function confirmDialogHandler(e: { detail: { action: 'delete' | 'cancel' } }) {
    if (e.detail.action === 'delete') {
        deleteUpdate(false);
    }
}

</script>

<div class="card" class:selected class:posted>
    <Dialog bind:this={confirmDeleteDialog} on:MDCDialog:closed={confirmDialogHandler}>
        <Title>Confirm Deletion</Title>
        <Content>Are you sure you want to delete this saved update?</Content>
        <Actions>
            <Button action="delete">
                <Label>DELETE</Label>
            </Button>
            <Button action="cancel" default use={[InitialFocus]}>
                <Label>CANCEL</Label>
            </Button>
        </Actions>
    </Dialog>
    <p style="display: flex;">
        <Icon class="material-icons" style="float: left; margin-right: 5px; font-size: 23px">chat</Icon>
        {@html update.body}
    </p>
    {#if scheduled}
        <p style="display: flex; align-items: center;">
            <Icon class="material-icons" style="float: left; margin-right: 5px; font-size: 23px">schedule</Icon>
            {'Posts ' + scheduledText}
        </p>
    {:else}
        <p style="display: flex; align-items: center;"
            use:tippy={realmNameTippyProps}>
            <Icon class="material-icons" style="float: left; margin-right: 5px; font-size: 23px">group</Icon>
            {realmName}
        </p>
    {/if}
    <Group style="width: 100%; margin-top: auto">
        <Button on:click={() => dispatch('edit')} disabled={selected}><Icon class="material-icons">edit</Icon><Label>Edit</Label></Button>
        {#if scheduled }
            <Button on:click={cancelUpdate}><Icon class="material-icons">cancel</Icon><Label>Cancel</Label></Button>
        {:else}    
            <Button on:click={() => deleteUpdate(true)}><Icon class="material-icons">delete</Icon><Label>Delete</Label></Button>
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

.card.posted {
    animation: green-flash 500ms ease backwards;
}

@keyframes green-flash {
    50% {
        background-color: rgb(109, 221, 109);
    }
    100% {
        background-color: white;
    }
}
</style>
