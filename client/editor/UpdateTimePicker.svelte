<script lang="ts">
import type { Update } from '../api/types';
import { momentToSchoologyTime, schoologyTimeToMoment } from '../api/types';
import '@smui/button/bare.css';
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import Flatpickr from '../utility/components/Flatpickr.svelte';
import type { Instance } from 'flatpickr/dist/types/instance';
import 'flatpickr/dist/flatpickr.css';
import moment from 'moment';

export let update: Update;

$: if (update.job === null) {
    update.job = { id: '' };
}
let flatpicker: Instance;
let scheduledFor = update.job?.scheduled_for;
let scheduledIn = update.job?.scheduled_in;

$: {
    update.job!.scheduled_in = undefined;
    update.job!.scheduled_for = scheduledFor;
}

$: {
    update.job!.scheduled_for = undefined;
    update.job!.scheduled_in = scheduledIn;
}
$: if (update.id) {
    if (update.job?.scheduled_for !== undefined) {
        flatpicker.setDate(update.job.scheduled_for, true);
    } else if (update.job?.scheduled_in !== undefined) {
        const createdAt = schoologyTimeToMoment(update.job.scheduled_at!);
        const postAt = momentToSchoologyTime(moment(createdAt).add(update.job.scheduled_in));
        flatpicker.setDate(postAt, true);
    }
}

let selectValue = 'on';
$: scheduledUpdateRelative = update.job?.scheduled_in || selectValue == 'in';

export function clear() {
    flatpicker.clear();
}

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
            <input bind:value={scheduledIn} />
        {:else}
            <!-- Datetime picker -->
            <Flatpickr options={flatpickrOptions} bind:fp={flatpicker} bind:formattedValue={scheduledFor} name="date" />
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
