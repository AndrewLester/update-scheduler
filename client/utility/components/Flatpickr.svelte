<script>
import { onMount, createEventDispatcher, onDestroy } from 'svelte';
import flatpickr from 'flatpickr';
const hooks = new Set([
    'onChange',
    'onOpen',
    'onClose',
    'onMonthChange',
    'onYearChange',
    'onReady',
    'onValueUpdate',
    'onDayCreate',
]);
export let value = '';
export let formattedValue = '';
export let element = null;
export let dateFormat = null;
export let placeholder = '';
export let options = {};
export let input = undefined
let fp;
$: if (fp) {
    fp.setDate(value, false, dateFormat);
}
onMount(() => {
    const elem = element || input;
    fp = flatpickr(
        elem,
        Object.assign(addHooks(options), element ? { wrap: true } : {})
    );
});

onDestroy(() => {
    if (fp) fp.destroy();
});

const dispatch = createEventDispatcher();
$: if (fp) {
    for (const [key, val] of Object.entries(addHooks(options))) {
        fp.set(key, val);
    }
}
function addHooks(opts = {}) {
    opts = Object.assign({}, opts);
    for (const hook of hooks) {
        const firer = (selectedDates, dateStr, instance) => {
            dispatch(stripOn(hook), [selectedDates, dateStr, instance]);
        };
        if (hook in opts) {
            // Hooks must be arrays
            if (!Array.isArray(opts[hook])) opts[hook] = [opts[hook]];
            opts[hook].push(firer);
        } else {
            opts[hook] = [firer];
        }
    }
    if (opts.onChange && !opts.onChange.includes(updateValue))
        opts.onChange.push(updateValue);
    return opts;
}
function updateValue(newValue, dateStr) {
    value =
        Array.isArray(newValue) && newValue.length === 1
            ? newValue[0]
            : newValue;
    formattedValue = dateStr;
}
function stripOn(hook) {
    return hook.charAt(2).toLowerCase() + hook.substring(3);
}

export function setDate(date, triggerChange) {
    fp.setDate(date, triggerChange);
}

export function clear() {
    fp.clear();
}
</script>

<input bind:this={input} {...$$restProps} {placeholder} />

<style>
input {
    font-size: inherit;
    width: 258px;
    border-radius: 10px;
    border: 1px solid gray;
    padding: 5px 10px;
}
</style>
