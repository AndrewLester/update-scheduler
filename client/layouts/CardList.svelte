<script lang="ts">
import { scale } from 'svelte/transition';
import { flip } from 'svelte/animate';
import { backOut, cubicIn } from 'svelte/easing';


type Identifiable = { id: any };

export let header: string;
export let items: any[];
export let horizontal = false;
</script>

<div class="card-list" class:horizontal>
    <h3>{header}</h3>
    {#if items}
        <div class="scrollable" class:horizontal>
            <div class="container">
                {#each items as item (item.id)}
                    <div class="item"
                        in:scale|local={{ start: 0.6, easing: backOut, duration: 250 }}
                        out:scale|local={{ start: 0.6, easing: cubicIn, duration: 250 }}
                        animate:flip={{ duration: 350 }}>
                        <slot {item} />
                    </div>
                {/each}
            </div>
        </div>
    {:else}
        <p style="font-style: italic;">No items</p>
    {/if}
</div>

<style>
.card-list {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    background-color: white;
    width: 100%;
    height: 100%;
    padding: 20px 1em;
    border-radius: 10px;
}

.card-list.horizontal {
    padding: 10px 1em;
}

.card-list > h3 {
    margin-top: 0px;
    text-align: center;
    color: black;
}

.card-list.horizontal > h3 {
    margin-bottom: 10px;
}

.scrollable {
    width: 100%;
    height: 100%;
    margin: 0px auto;
    border-radius: 5px;
    overflow-y: auto;
    box-shadow: inset 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
    background-color: var(--main-background-color);
}

.scrollable.horizontal {
    width: 80%;
    height: auto;
    overflow-x: auto;
}

.container {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    width: 100%;
    height: auto;
    float: left;
    gap: 20px;
    padding: 20px 10px;
}

.scrollable.horizontal > .container {
    flex-flow: row nowrap;
    width: auto;
    padding: 10px 20px;
}

</style>
