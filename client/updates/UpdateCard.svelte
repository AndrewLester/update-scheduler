<script lang="ts">
import Button, { Group, Icon } from '@smui/button/bare';
import '@smui/button/bare.css';
import type { Update } from '../api/types';

export let update: Update;

</script>

<div class="card">
    <p>{update.body}</p>
    <Group variant={'outlined'} style="width: 100%">
        <Button><Icon class="material-icons">favorite</Icon></Button>
        <Button><Icon class="material-icons">clock</Icon></Button>
    </Group>
</div>

<style>
.card {
    display: flex;
    flex-flow: column nowrap;
    align-items: stretch;
    height: 100px;
    width: 150px;
    max-height: 100%;
    border-radius: 5px;
    background: hotpink;
}
</style>