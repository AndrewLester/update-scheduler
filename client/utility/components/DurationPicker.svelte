<script lang="ts">
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import moment from 'moment';

export let scheduledAt: string | undefined;
export let scheduledIn: string;

type DurationType = 'minute' | 'hour' | 'day';

let selectValue: DurationType = scheduledIn ? getTimeUnit(moment.duration(scheduledIn)) : 'minute';
let inputValue: number | undefined = scheduledIn ? moment.duration(scheduledIn).as(selectValue) : undefined;

$: if (inputValue) {
    scheduledIn = moment.duration(inputValue, selectValue).toISOString();
}

export function clear() {
    inputValue = undefined;
    selectValue = 'minute';
}

function getTimeUnit(duration: moment.Duration): DurationType {
    return duration.humanize().split(' ')[1] as DurationType;
}

function pluralize(word: string, quantity: number) {
    if (quantity !== 1) {
        return word + 's';
    }
    return word;
}
</script>

<div class="duration-picker">
    <input class="duration-input" bind:value={inputValue} type="number" placeholder="Enter a duration" />
    <Select variant="filled" bind:value={selectValue} class="select" anchor$class="select-width select-height" menu$class="select-width">
        <Option value="minute">{pluralize('minute', inputValue ?? 0)}</Option>
        <Option value="hour">{pluralize('hour', inputValue ?? 0)}</Option>
        <Option value="day">{pluralize('day', inputValue ?? 0)}</Option>
    </Select>
</div>


<style>
.duration-picker {
    display: flex;
    flex-flow: row nowrap;
    flex-direction: row;
    align-items: center;
}
.duration-input {
    font-size: inherit;
    width: 175px;
    border-radius: 10px;
    border: 1px solid gray;
    padding: 5px 10px;
    margin-right: 10px;
    outline: none;
}
.duration-picker :global(.select-width) {
    width: 115px;
    min-width: 115px;
}
</style>