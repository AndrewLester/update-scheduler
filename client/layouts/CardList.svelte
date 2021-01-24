<script lang="ts">
import { scale } from 'svelte/transition';
import { flip } from 'svelte/animate';
import { backOut, cubicIn } from 'svelte/easing';


type Identifiable = { id: any };

export let header: string;
export let items: any[];
export let horizontal = false;
</script>

<div class="card-list">
    <h3>{header}</h3>
    <div class="container" class:horizontal>
        {#each items as item (item.id)}
            <div class="item"
                in:scale={{ start: 0.6, easing: backOut, duration: 250 }}
                out:scale={{ start: 0.6, easing: cubicIn, duration: 250 }}
                animate:flip={{ duration: 350 }}>
                <slot {item} />
            </div>
        {/each}
    </div>
</div>

<style>
.card-list {
    background-color: white;
    width: 100%;
    height: 100%;
    border-radius: 10px;
}

.card-list > h3 {
    margin-top: 0px;
    text-align: center;
    color: black;
    font-weight: bold;
}

.container {
    display: flex;
    flex: column no-wrap;
    height: auto;
    width: 100%;
    margin: 0px auto;
    background-color: var(--main-background-color);
}

.container.horizontal {
    flex: row no-wrap;
    width: 80%;
    margin: 0px auto;
}

</style>