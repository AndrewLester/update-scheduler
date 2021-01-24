<script lang="ts">
import Button, { Label } from '@smui/button/bare';
import '@smui/button/bare.css';
import Textfield from '@smui/textfield/bare';
import '@smui/textfield/bare.css';

let value: string = '';
</script>

<div class="editor">
    <Textfield fullwidth textarea bind:value={value} label="Write update" input$aria-controls="helper-text-fullwidth-textarea" input$aria-describedby="helper-text-fullwidth-textarea" />
    <Button variant="outlined"><Label>Save</Label></Button>
    <Button variant="raised"><Label>Save and Schedule</Label></Button>
</div>


<style>
.editor {
    border-radius: 15px;
    background: white;
    padding: 20px 40px;
}
</style>