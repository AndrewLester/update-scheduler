<script lang="ts">
import type { ScheduledJob, Update } from '../api/types';
import '@smui/button/bare.css';
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import Flatpickr from '../utility/components/Flatpickr.svelte';
import DurationPicker from '../utility/components/DurationPicker.svelte';
import 'flatpickr/dist/flatpickr.css';

export let job: ScheduledJob;

let flatpicker: Flatpickr;
let durationPicker: DurationPicker | undefined;
let scheduledUpdateRelative = !!job.scheduled_in;
let selectValue = scheduledUpdateRelative ? 'in' : 'on';

$: if (job.scheduled_for && !scheduledUpdateRelative) {
    job.scheduled_in = undefined;
    if (flatpicker) {
        flatpicker.setDate(job.scheduled_for, true);
    }
}
$: if (job.scheduled_in && scheduledUpdateRelative) job.scheduled_for = undefined;

$: scheduledUpdateRelative = selectValue === 'in';

const flatpickrOptions = {
    enableTime: true,
    altInput: true,
    altFormat: 'F j, Y at h:i K',
    dateFormat: 'Y-m-d H:i:S',
    minDate: 'today',
    position: 'below left',
    static: true,
    onOpen: handleFlatpickrOpen
}

async function handleFlatpickrOpen(_, __, fp) {
    fp.calendarContainer.scrollIntoView({ behavior: 'smooth' });
}

export function clear() {
    if (flatpicker) flatpicker.clear();
    if (durationPicker) durationPicker.clear();
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
            <DurationPicker bind:duration={job.scheduled_in} bind:this={durationPicker} durationStart={job.scheduled_at} />
        {:else}
            <!-- Datetime picker -->
            <Flatpickr
                options={flatpickrOptions}
                placeholder={'Choose a date'}
                bind:this={flatpicker}
                bind:formattedValue={job.scheduled_for}
                name="date" />
        {/if}
    </div>
</div>

<style>
.picker {
    display: flex;
    flex-flow: row wrap;
    align-items: center;
    gap: 5px 0px;
    margin: 10px 0px;
}

.picker > * {
    margin: 0px 10px;
}

.picker > :global(.select) :global(.select-width) {
    width: 75px;
    min-width: 75px;
}
</style>
