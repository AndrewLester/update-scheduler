<script lang="ts">
import Textfield from '@smui/textfield/bare';
import '@smui/textfield/bare.css';

let value: string = '';
</script>

<div class="editor">
    <Textfield fullwidth textarea bind:value={value} label="Write update" input$aria-controls="helper-text-fullwidth-textarea" input$aria-describedby="helper-text-fullwidth-textarea" />
</div>


<style>
.editor {
    border-radius: 20px;
    background: white;
    padding: 20px 40px;
}
</style>