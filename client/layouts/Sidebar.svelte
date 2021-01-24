<script lang="ts">

type Side = 'left' | 'right';

export let side: Side;

</script>

<div class="container" class:left={side === 'left'} class:right={side === 'right'}>

</div>

<style>
.container {
    height: 100%;
    width: 100%;
    background: white;
}

.container.left {
    border-radius: 0px 15px 15px 0px;
}

.container.right {
    border-radius: 15px 0px 0px 15px;
}
</style>