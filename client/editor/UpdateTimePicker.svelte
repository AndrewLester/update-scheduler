<script lang="ts">
import type { Update } from '../api/types';
import { momentToSchoologyTime, schoologyTimeToMoment } from '../api/types';
import '@smui/button/bare.css';
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import Flatpickr from '../utility/components/Flatpickr.svelte';
import DurationPicker from '../utility/components/DurationPicker.svelte';
import type { Instance } from 'flatpickr/dist/types/instance';
import 'flatpickr/dist/flatpickr.css';
import { tick } from 'svelte';

export let update: Update;

$: if (update.job === null) {
    update.job = { id: '' };
}
$: id = update.id;
let flatpicker: Instance | undefined;
const getFlatPicker = () => flatpicker!;
let durationPicker: DurationPicker | undefined;
let scheduledFor = update.job?.scheduled_for;
let scheduledIn = update.job?.scheduled_in;
let scheduledUpdateRelative = !!update.job?.scheduled_in;
let selectValue = scheduledUpdateRelative ? 'in' : 'on';
const getScheduledFor = () => update.job?.scheduled_for!;
const getScheduledIn = () => update.job?.scheduled_in;
// $: update.job!.scheduled_for = scheduledFor;
$: update.job!.scheduled_in = scheduledIn;
$: scheduledUpdateRelative = selectValue === 'in';
// Clear the flatpicker object that was bound to the element once the element is gone
$: if (scheduledUpdateRelative) flatpicker = undefined;
$: console.log('Update sheduled for:', update.job?.scheduled_for, 'Update scheduled in:', update.job?.scheduled_in, 'Scheduled Update relative:', scheduledUpdateRelative, 'Select value:', selectValue);
// React to changes in `update`
$: if (id) {
    if (isUpdateRelative()) {
        selectValue = 'in';
        scheduledIn = getScheduledIn();
    } else {
        selectValue = 'on';
        tick().then(() => {
            getFlatPicker().setDate(getScheduledFor(), true);
        });
    }
}

export function clear() {
    if (flatpicker) {
        flatpicker.clear();
    } else if (durationPicker) {
        durationPicker.clear();
    }
}

function isUpdateRelative() {
    return !!update.job?.scheduled_in;
}

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
            <DurationPicker bind:scheduledIn bind:this={durationPicker} scheduledAt={update.job?.scheduled_at} />
        {:else}
            <!-- Datetime picker -->
            <Flatpickr
                options={flatpickrOptions}
                placeholder={'Choose a date'}
                bind:fp={flatpicker}
                bind:formattedValue={scheduledFor}
                name="date" />
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

.picker > :global(.select) :global(.select-width) {
    width: 75px;
    min-width: 75px;
}
</style>
