<script lang="ts" context="module">
export const gridAreas = {
    minimal: {
        areas: `"left-sidebar main main"
                "left-sidebar main main"`,
        transitions: [],
        rank: 0
    },
    rightsidebar: {
        areas: `"left-sidebar main right-sidebar"
                   "left-sidebar main right-sidebar"`,
        transitions: [
            {
                'right-sidebar': 250
            }
        ],
        rank: 1
    },
    bottombar: {
        areas: `"left-sidebar main main"
                "left-sidebar bottombar bottombar"`,
        transitions: [
            {
                bottombar: 250
            }
        ],
        rank: 1
    },
    maximum: {
        areas: `"left-sidebar main right-sidebar"
               "left-sidebar bottombar right-sidebar"`,
        transitions: [
            {
                'right-sidebar': 250
            },
            {
                bottombar: 250
            }
        ],
        rank: 2
    }
}

export type GridArea = keyof typeof gridAreas;
</script>

<script lang="ts">
import { tick } from "svelte";

import { sleep, svelteTransitionEnd } from "../utility/async";


export let areas: GridArea;
let currentAreas: GridArea = areas;
const getCurrentAreas = () => currentAreas;
let main: HTMLElement;

$: (async () => {
    if (main) {
        if (gridAreas[areas].rank <= gridAreas[getCurrentAreas()].rank) {
            for (const transition of gridAreas[getCurrentAreas()].transitions) {
                const parentElement = main.querySelector('.' + Object.keys(transition)[0]);

                (main.firstElementChild! as HTMLElement).style.maxHeight = `calc(100% + ${parentElement?.clientHeight}px)`;
                if (parentElement?.firstElementChild) {
                    await svelteTransitionEnd(parentElement.firstElementChild, 300);
                }
                const oldTransition = (main.firstElementChild! as HTMLElement).style.transition;
                (main.firstElementChild! as HTMLElement).style.transition = 'none';
                (main.firstElementChild! as HTMLElement).style.maxHeight = '100%';
                // Use requestAnimationFrame to reset transition property after
                // Height has transitioned to the right spot. This prevents a 
                // Reverse transition after the height is switched by the grid
                requestAnimationFrame(() => {
                    (main.firstElementChild! as HTMLElement).style.transition = oldTransition;
                });
            }
        } else {
            (main.firstElementChild! as HTMLElement).style.maxHeight = '';
        }

        // Setting main.style directly causes a cyclical state update
        const styleObject = main.style;
        styleObject.gridTemplateAreas = gridAreas[areas].areas;
        currentAreas = areas;
    }
})();

</script>

<main bind:this={main} class={areas}>
    <div class="main">
        <slot name="main"></slot>
    </div>
    <div class="bottombar">
        <slot name="bottombar"></slot>
    </div>
    <div class="left-sidebar">
        <slot name="left-sidebar"></slot>
    </div>
    <div class="right-sidebar">
        <slot name="right-sidebar"></slot>
    </div>
</main>

<style>
main {
    display: grid;
    grid-template-columns: 1fr 3fr 1fr;
    grid-template-rows: 2fr 1.25fr;
    grid-template-areas:
              "left-sidebar main main"
              "left-sidebar main main";
    gap: 0px 25px;
    height: calc(100vh - var(--header-height));
    overflow-y: hidden;
    width: 100vw;
    padding: 20px 0px;
    background-color: var(--main-background-color);
}

main > * {
    height: 100%;
    width: 100%;
}

main.maximum > .main, main.bottombar > .main {
    max-height: calc(100% - 20px);
}

/* main.minimal > .main {
    max-height: 100%;
} */

.main {
    grid-area: main;
    transition: max-height 250ms ease;
    height: 200%;
    max-height: 100%;
}

.bottombar {
    grid-area: bottombar;
}

.left-sidebar {
    grid-area: left-sidebar;
}

.right-sidebar {
    grid-area: right-sidebar;
}
</style>