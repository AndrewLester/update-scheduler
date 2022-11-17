<script lang="ts">
import { onMount } from 'svelte';

import { quill } from '../quill';

export let content: string;
export let placeholder: string;

let editor: HTMLElement | undefined;

onMount(() => {
    editor!.firstElementChild!.innerHTML = content;
});

export function setContent(newContent: string) {
    if (editor && editor.firstElementChild) {
        editor.firstElementChild.innerHTML = newContent;
    }
}

export function clear() {
    setContent('');
}
</script>

<div
    class="editor"
    bind:this={editor}
    use:quill={{ placeholder }}
    on:text-change={(e) => (content = e.detail.html)} />

<style>
.editor {
    overflow-x: visible;
    font-family: inherit;
    font-size: inherit;
    height: unset !important;
}

.editor :global(.ql-editor) {
    min-height: 200px;
}

.editor :global(.ql-tooltip[data-mode='video']::before) {
    content: 'Enter web page or video:';
}
</style>
