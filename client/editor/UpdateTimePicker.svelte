<script lang="ts">
import type { Update } from '../api/types';
import '@smui/button/bare.css';
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import Flatpickr from '../utility/components/Flatpickr.svelte';
import type { Instance } from 'flatpickr/dist/types/instance';
import 'flatpickr/dist/flatpickr.css';

export let update: Update;

$: if (!update.job) {
    update.job = { id: '', scheduled_for: undefined, scheduled_in: undefined }
}

let flatpicker: Instance;
let scheduledAt: string;

let scheduledIn: string;
$: if (update.job) {
    update.job.scheduled_for = scheduledAt;
}

let selectValue = 'on';
$: scheduledUpdateRelative = update.job?.scheduled_in || selectValue == 'in';


const flatpickrOptions = {
    enableTime: true,
    altInput: true,
    altFormat: 'F j, Y at h:i K',
    dateFormat: 'Y-m-d H:i:S',
    minDate: 'today'
}
</script>

<div class="picker">
    <div class="picker-text">Post</div>
    <Select variant="filled" bind:value={selectValue} class="select" anchor$class="select-width select-height" menu$class="select-width">
        <Option value="on">on</Option>
        <Option value="in">in</Option>
    </Select>
    <div class="picker-text">
        {#if scheduledUpdateRelative }
            <!-- Duration picker -->
        {:else}
            <!-- Datetime picker -->
            <Flatpickr options={flatpickrOptions} bind:flatpicker bind:formattedValue={scheduledAt} name="date" />
        {/if}
    </div>
</div>

<style>
.picker {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    gap: 5px 0px;
    margin: 10px 0px;
}

.picker > * {
    margin: 0px 10px;
}

.picker :global(.select-width) {
    width: 75px;
    min-width: 75px;
}
</style>