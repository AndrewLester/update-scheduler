<script lang="ts">
import { fly, slide } from 'svelte/transition';
import type { Attachment } from "../api/types";
import { flip } from 'svelte/animate';
import Dialog from '@smui/dialog/Dialog.svelte';
import { Title, Content, Actions, InitialFocus } from '@smui/dialog/bare';
import List, {Item, Graphic, Text, PrimaryText, SecondaryText, Meta} from '@smui/list/bare';
import '@smui/list/bare.css';
import '@smui/dialog/bare.css';
import IconButton from '@smui/icon-button/bare';
import '@smui/icon-button/bare.css';
import Button, { Label, Icon } from '@smui/button/bare';
import '@smui/button/bare.css';
import AttachmentEditor from '../editor/AttachmentEditor.svelte';
import OpenGraphView from '../utility/components/OpenGraphView.svelte';

export let attachments: Attachment[];
let editableAttachments = attachments;

let dialog: Dialog;
let editing: Attachment | undefined;

export function open() {
    editableAttachments = attachments;
    dialog.open();
}

function dialogActionHandler(e: { detail: { action: 'add' | 'cancel' } }) {
    if (e.detail.action === 'cancel') return;

    attachments = editableAttachments;
    editing = undefined;
    editableAttachments = [];
}

function deleteAttachment(attachment: Attachment) {
    editableAttachments = editableAttachments.filter((a) => a !== attachment);
}

function editAttachment(attachment: Attachment) {
    editing = attachment;
}

function createAttachment() {
    const attachment: Attachment = {
        id: -1,
        type: 'link',
        url: '',
        title: ''
    }

    editAttachment(attachment);
}

function saveAttachment(attachment?: Attachment) {
    if (!attachment) return;

    const index = editableAttachments.indexOf(attachment);
    if (index > -1) {
        editableAttachments.splice(editableAttachments.indexOf(attachment), 1, attachment);
    } else {
        editableAttachments.push(attachment);
    }

    editableAttachments = editableAttachments;
    editing = undefined;
}

const icons = {
    link: 'link',
    video: 'videocam'
}
</script>

<Dialog
    bind:this={dialog}
    on:MDCDialog:closed={dialogActionHandler}>
    <Title>
        {#if editing}
            Add an attachment
        {:else}
            View attachments
        {/if}
    </Title>
    <Content id="attachment-dialog">
        {#if editing}
            <div
                transition:fly={{duration: 350, x: 500}}>
                <AttachmentEditor attachment={editing}
                    on:save={() => saveAttachment(editing)}
                    on:discard={() => editing = undefined} />
            </div>
        {:else}
            <div
                transition:fly={{duration: 350, x: -500}}>
                <div class="attachment-list">
                    <List twoLine avatarList>
                        {#each editableAttachments as attachment (attachment)}
                            <div style="display: flex; flex-flow: row nowrap; margin-top: 10px;"
                                animate:flip={{ duration: 250, delay: 350 }}>
                                <OpenGraphView alternativeIcon={icons[attachment.type]} data={{
                                    ...attachment,
                                    description: attachment.summary
                                }} />
                                <div style="display: flex; flex-flow: column nowrap; margin-left: 10px; justify-content: space-evenly;">
                                    <IconButton
                                        class="material-icons"
                                        on:click={() => editAttachment(attachment)}>
                                        edit
                                    </IconButton>
                                    <IconButton
                                        class="material-icons"
                                        on:click={() => deleteAttachment(attachment)}>
                                        delete
                                    </IconButton>
                                </div>
                            </div>
                        {:else}
                            <p  transition:slide
                                style="text-align: center; height: 72px">No attachments</p>
                        {/each}
                    </List>
                </div>
                <div class="button-row">
                    <Button variant="outlined" on:click={() => createAttachment()}>
                        ADD ATTACHMENT
                    </Button>
                </div>
            </div>
        {/if}
    </Content>
    <Actions>
        {#if !editing}
            <Button action="cancel">
                <Label>CANCEL</Label>
            </Button>
            <Button action="add" default use={[InitialFocus]}>
                <Label>SAVE</Label>
            </Button>
        {/if}
    </Actions>
</Dialog>

<style>
:global(#attachment-dialog) {
    display: grid;
    grid-auto-columns: 100%;
    grid-auto-rows: 100%;
    max-width: 80vw;
    max-height: calc(calc(100vh - var(--header-height)) - 180px);
    width: 500px;
    height: 100%;
    overflow-x: hidden;
}
:global(#attachment-dialog) > :global(div) {
    grid-column: 1;
    grid-row: 1;
    width: 100%;
}
:global(#attachment-dialog) :global(.button-row) {
    margin-top: 10px;
}
</style>