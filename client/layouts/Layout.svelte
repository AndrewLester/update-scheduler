<script lang="ts" context="module">
export const gridAreas = {
    minimal: {
        areas: `"left-sidebar main main"
                "left-sidebar main main"`,
        transitions: [] as Transition[],
        rank: 0,
    },
    rightsidebar: {
        areas: `"left-sidebar main right-sidebar"
                "left-sidebar main right-sidebar"`,
        transitions: [
            {
                original: 'right-sidebar',
                replacement: 'main',
                duration: 300,
                transitionFunction: rightSidebarTransition,
            },
        ] as Transition[],
        rank: 1,
    },
    bottombar: {
        areas: `"left-sidebar main main"
                "left-sidebar bottombar bottombar"`,
        transitions: [
            {
                original: 'bottombar',
                replacement: 'main',
                duration: 300,
                transitionFunction: bottomBarTransition,
            },
        ] as Transition[],
        rank: 1,
    },
    maximum: {
        areas: `"left-sidebar main right-sidebar"
                "left-sidebar bottombar right-sidebar"`,
        transitions: [
            {
                original: 'right-sidebar',
                replacement: 'main',
                duration: 300,
                transitionFunction: rightSidebarTransition,
            },
            {
                original: 'right-sidebar',
                replacement: 'bottombar',
                duration: 300,
                transitionFunction: rightSidebarTransition,
            },
            {
                original: 'bottombar',
                replacement: 'main',
                duration: 300,
                transitionFunction: bottomBarTransition,
            },
        ] as Transition[],
        rank: 2,
    },
};

export type GridArea = keyof typeof gridAreas;
</script>

<script lang="ts">
import { setContext, tick } from 'svelte';

import {
    bottomBarTransition,
    rightSidebarTransition,
} from './layout_transitions';
import type { Transition } from './layout_transitions';

export let areas: GridArea;

let currentAreas: GridArea = areas;
const getCurrentAreas = () => currentAreas;
setContext('layoutContext', getCurrentAreas);

let main: HTMLElement;

$: (async () => {
    if (main) {
        let delayedTransitionElements = [] as HTMLElement[];

        if (gridAreas[areas].rank == gridAreas[getCurrentAreas()].rank) {
            for (const transition of gridAreas[areas].transitions) {
                tick().then(() => {
                    // Replacement = original because the new transitions would be happening forwards
                    // rather than the default of backwards
                    const replacementElement = main.querySelector(
                        '.' + transition.original
                    ) as HTMLElement;

                    // Hide replacement element since it now has children so it won't be hidden by CSS
                    replacementElement.style.width = '0px';
                    replacementElement.style.height = '0px';
                    delayedTransitionElements.push(replacementElement);
                });
            }

            await layoutOutTransitions();
        } else if (gridAreas[areas].rank < gridAreas[getCurrentAreas()].rank) {
            await layoutOutTransitions();
        }

        // Setting main.style directly causes a cyclical state update
        const styleObject = main.style;
        styleObject.gridTemplateAreas = gridAreas[areas].areas;
        currentAreas = areas;
        delayedTransitionElements.forEach((elem) => {
            // Restore paused elements sizes before their in transitions play
            elem.style.width = '';
            elem.style.height = '';
        });
    }
})();

async function layoutOutTransitions() {
    let transitions = [] as Promise<void>[];
    for (const transition of gridAreas[getCurrentAreas()].transitions) {
        // If the new layout has the original element, don't transition it out
        if (gridAreas[areas].areas.includes(transition.original)) {
            continue;
        }

        const originalElement = main.querySelector(
            '.' + transition.original
        ) as HTMLElement;
        const replacementElement = main.querySelector(
            '.' + transition.replacement
        ) as HTMLElement;

        transitions.push(
            transition.transitionFunction(
                originalElement,
                replacementElement,
                transition.duration
            )
        );
    }
    await Promise.all(transitions);
}

export function getElementTransitionDelay(
    layoutArea: string,
    newArea: GridArea
) {
    const newAreas = gridAreas[newArea];
    if (newAreas.rank != gridAreas[getCurrentAreas()].rank) return;

    const transition = newAreas.transitions.find(
        (t) => t.original === layoutArea
    );
    return transition?.duration;
}
</script>

<main bind:this={main} class={areas}>
    <div class="main">
        <slot name="main" />
    </div>
    <div class="bottombar">
        <slot name="bottombar" />
    </div>
    <div class="left-sidebar">
        <slot name="left-sidebar" />
    </div>
    <div class="right-sidebar">
        <slot name="right-sidebar" />
    </div>
</main>

<style>
main {
    display: grid;
    grid-template-columns: 1fr minmax(0, 3fr) 1fr;
    grid-template-rows: minmax(0, 2fr) 1.25fr;
    grid-template-areas:
        'left-sidebar main main'
        'left-sidebar main main';
    gap: 0px 25px;
    height: calc(100vh - var(--header-height));
    overflow: hidden;
    width: 100vw;
    padding: 20px 0px;
    background-color: var(--main-background-color);
}

main > * {
    height: 100%;
    width: 100%;
}

.bottombar:empty {
    display: none;
}

main.maximum > .main,
main.bottombar > .main {
    max-height: calc(100% - 20px);
}

.main {
    grid-area: main;
    max-height: 100%;
    max-width: 100%;
}

.bottombar {
    grid-area: bottombar;
    max-width: 100%;
}

.left-sidebar {
    grid-area: left-sidebar;
}

.right-sidebar {
    grid-area: right-sidebar;
}
</style>
