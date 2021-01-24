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
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    background-color: white;
    width: 100%;
    height: 100%;
    padding: 20px 10px;
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
    flex-flow: column nowrap;
    align-items: center;
    width: 100%;
    height: 100%;
    padding: 20px 10px;
    border-radius: 5px;
    overflow-y: auto;
    box-shadow: inset 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
    margin: 0px auto;
    background-color: var(--main-background-color);
}

.container.horizontal {
    flex-flow: row nowrap;
    width: 80%;
    padding: 10px 20px;
    height: auto;
    margin: 0px auto;
}

</style>