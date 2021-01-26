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
    <div class="scrollable" class:horizontal>
        <div class="container">
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

.card-list > h3 {
    margin-top: 0px;
    text-align: center;
    color: black;
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
    overflow-y: auto;
}

.container {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    width: auto;
    height: auto;
    float: left;
    gap: 20px;
    padding: 20px 10px;
}

.scrollable.horizontal > .container {
    flex-flow: row nowrap;
    padding: 10px 20px;
}

</style>