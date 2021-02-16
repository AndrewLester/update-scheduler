<script lang="ts">
import { quill } from '../quill';

export let content: string;
export let placeholder: string;

let editor: HTMLElement | undefined;

const options = {
    modules: {
        toolbar: [
            [{ header: [1, 2, 3, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            ['link', 'image']
        ]
    },
    placeholder: placeholder,
    theme: 'snow',
};

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
    use:quill={options}
    on:text-change={(e) => (content = e.detail.html)} />

<style>
.editor {
    resize: vertical;
    overflow-y: auto;
    overflow-x: visible;
    height: 100px;
    font-family: inherit;
    font-size: inherit;
    
}
/* .editor :global(.ql-editor) {
    height: 100% !important;
}  */
</style>
