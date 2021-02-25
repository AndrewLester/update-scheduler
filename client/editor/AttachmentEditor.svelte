<script lang="ts">
import Button, { Label, Icon } from '@smui/button/bare';
import '@smui/button/bare.css';
import type { Attachment } from '../api/types';

export let attachments: Attachment[];


</script>

<div class="attachment-editor">
    <Button variant="outlined" on:click>
        <Icon class="material-icons">add</Icon>
        <Label>Add an attachment</Label>
    </Button>
    {#each attachments as attachment (attachment.id)}
        <!-- <Attachment {attachment} /> -->
        <p>{attachment.title}</p>
    {/each}
</div>

<style>

</style>