<script lang="ts">
import Button, { Label, Icon } from '@smui/button/bare';
import '@smui/button/bare.css';
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import type { Attachment } from '../api/types';

export let attachments: Attachment[];

let selectValue = 'on';

</script>

<div class="attachment-editor">
    Attach
    <Select variant="filled" bind:value={selectValue} class="select" anchor$class="select-width select-height" menu$class="select-width">
        <Option value="link">link</Option>
        <Option value="video">video</Option>
    </Select>
    {#each attachments as attachment (attachment.id)}
        <!-- <Attachment {attachment} /> -->
        <p>{attachment.title}</p>
    {/each}
</div>

<style>
.picker > :global(.select) :global(.select-width) {
    width: 75px;
    min-width: 75px;
}
</style>