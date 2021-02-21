<script lang="ts">
import Select, { Option } from '@smui/select/bare';
import '@smui/select/bare.css';
import moment from 'moment';
import { momentToSchoologyTime, schoologyTimeToMoment } from '../../api/types';
import { time } from '../../stores';

export let duration: string;
export let durationStart: string | undefined;

type DurationType = 'minute' | 'hour' | 'day';

let inputValue: number | undefined = undefined;
let selectValue: DurationType = duration ? getTimeUnit(moment.duration(duration)) : 'minute';

$: minutes = moment($time).seconds(0).milliseconds(0)
if (duration) {
    if (durationStart) {
        const scheduledAtMoment = schoologyTimeToMoment(durationStart);
        const scheduledInDuration = moment.duration(duration);
        const postTime = scheduledAtMoment.add(scheduledInDuration);
        inputValue = moment.duration(postTime.diff(minutes)).as(selectValue).toFixed(2);
    }
    // TODO: Handle case with no durationStart
}

$: if (inputValue) {
    duration = moment.duration(inputValue, selectValue).toISOString();
}

export function clear() {
    inputValue = undefined;
    selectValue = 'minute';
}

function getTimeUnit(durationMoment: moment.Duration): DurationType {
    if (durationMoment.asDays() % 1 === 0) {
        return 'day';
    } else if (durationMoment.asHours() % 1 === 0) {
        return 'hour';
    } else {
        return 'minute';
    }
}

function pluralize(word: string, quantity: number) {
    if (quantity !== 1) {
        return word + 's';
    }
    return word;
}
</script>

<div class="duration-picker">
    <input class="duration-input" bind:value={inputValue} type="number" placeholder="Enter a duration" max="1000" min="0" />
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
