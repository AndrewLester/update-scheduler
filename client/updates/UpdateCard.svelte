<script lang="ts">
import Button, { Group, Icon, Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import Dialog from '@smui/dialog/Dialog.svelte';
import { Title, Content, Actions, InitialFocus } from '@smui/dialog/bare';
import '@smui/dialog/bare.css';
import moment from 'moment';
import { createEventDispatcher } from 'svelte';
import type { Update } from '../api/types';
import { schoologyTimeToMoment } from '../api/types';
import { isScheduled, momentToSchoologyTime } from '../api/types';
import { realms, time, updates } from '../stores';
import tippy from '../utility/tippy';
import 'tippy.js/animations/shift-away-subtle.css';

export let update: Update;
export let selected: boolean;

let confirmDeleteDialog: Dialog;

let posted = false;
let resets = 0;

$: scheduled = isScheduled(update);
$: realmName = ($realms.find((realm) => realm.id === update.realm_id) || {}).name;
let scheduledText = '';
const resetJob = () => (update.job = null);
$: if (scheduled) {
    let timeUntilPost: moment.Duration | undefined;
    if (update.job && update.job!.scheduled_in) {
        const postsAt = schoologyTimeToMoment(update.job!.scheduled_at!).add(
            moment.duration(update.job!.scheduled_in)
        );
        timeUntilPost = moment.duration(postsAt.diff($time));
    } else if (update.job && update.job!.scheduled_for) {
        timeUntilPost = moment.duration(
            schoologyTimeToMoment(update.job!.scheduled_for).diff($time)
        );
    }

    if (timeUntilPost !== undefined) {
        if (timeUntilPost.asMilliseconds() <= 0) {
            posted = true;
            scheduledText = 'Just posted';
            resetJob();
        } else {
            scheduledText = 'Posts ' + timeUntilPost.humanize(true, {ss: 0});
        }
    } else {
        // Only try resetting the updates store every 5 seconds because it sends a GET request.
        if ($time.seconds() % 5 === 0 && resets < 3) {
            updates.reset();
            resets++;
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
    trigger: 'mouseenter',
};

let postTimeInfo: string;
$: if (isScheduled(update) && update.job) {
    if (update.job!.scheduled_for) {
        postTimeInfo = 'Posts at: ' + update.job!.scheduled_for;
    } else {
        postTimeInfo = 'Posts at: ' +
            schoologyTimeToMoment(update.job!.scheduled_at!)
            .add(moment.duration(update.job!.scheduled_in)).format('YYYY-MM-DD HH:mm:ss');
    }
}
$: postTimeTippyProps = {
    content: postTimeInfo,
    placement: 'right',
    arrow: true,
    duration: [100, 100],
    animation: 'shift-away-subtle',
    touch: ['hold', 450],
    trigger: 'mouseenter',
};

const updateBodyTippyProps = {
    content: 'Certain styles might not be visible',
    placement: 'right',
    arrow: true,
    duration: [100, 100],
    animation: 'shift-away-subtle',
    touch: ['hold', 450],
    trigger: 'mouseenter',
};

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
    dispatch('cancel');

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
    <Dialog
        bind:this={confirmDeleteDialog}
        on:MDCDialog:closed={confirmDialogHandler}>
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
    <p  class="body one-line-parent" use:tippy={updateBodyTippyProps}>
        <Icon
            class="material-icons"
            style="float: left; margin-right: 5px; font-size: 23px">
            chat
        </Icon>
        {@html update.body}
    </p>
    {#if scheduled}
        <p class="one-line" use:tippy={postTimeTippyProps}>
            <Icon
                class="material-icons"
                style="float: left; margin-right: 5px; font-size: 23px">
                schedule
            </Icon>
            {scheduledText}
        </p>
    {:else}
        <p  class="one-line"
            use:tippy={realmNameTippyProps}>
            <Icon
                class="material-icons"
                style="float: left; margin-right: 5px; font-size: 23px">
                group
            </Icon>
            {realmName || 'Loading...'}
        </p>
    {/if}
    <Group style="width: 100%; margin-top: auto" variant="outlined">
        <Button on:click={() => dispatch('edit')} disabled={selected} variant="outlined">
            <Icon class="material-icons">edit</Icon>
            <Label>Edit</Label>
        </Button>
        {#if scheduled}
            <Button on:click={cancelUpdate} variant="outlined">
                <Icon class="material-icons">cancel</Icon>
                <Label>Cancel</Label>
            </Button>
        {:else}
            <Button on:click={() => deleteUpdate(true)} variant="outlined">
                <Icon class="material-icons">delete</Icon>
                <Label>Delete</Label>
            </Button>
        {/if}
    </Group>
</div>

<style>
.card {
    display: flex;
    flex-flow: column nowrap;
    align-items: stretch;
    height: 100px;
    width: auto;
    max-width: 175px;
    max-height: 100%;
    border-radius: 5px;
    background: white;
}

p {
    max-height: 100%;
    padding: 5px 5px;
    overflow: hidden;
    text-overflow: ellipsis;
    overflow-wrap: break-word;
}

p > :global(*) {
    vertical-align: top;
}

p.one-line {
    white-space: nowrap;
}

p.one-line-parent > :global(p) {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

p.body :global(*:not(i)) {
    margin: 0px !important;
    padding: 0px !important;
    font-size: 16px !important;
}

p.body {
    max-height: 40px;
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
