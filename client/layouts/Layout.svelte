<script lang="ts" context="module">
export const gridAreas = {
    minimal: `"left-sidebar main main"
              "left-sidebar main main"`,
    rightsidebar: `"left-sidebar main right-sidebar"
                   "left-sidebar main right-sidebar"`,
    bottombar: `"left-sidebar main main"
                "left-sidebar bottombar bottombar"`,
    maximum: `"left-sidebar main right-sidebar"
              "left-sidebar bottombar right-sidebar"`
}

export type GridArea = keyof typeof gridAreas;
</script>

<script lang="ts">

export let areas: GridArea;


let main: HTMLElement;

$: if (main) {
    main.style.gridTemplateAreas = gridAreas[areas];
}

</script>

<main bind:this={main}>
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
    grid-template-rows: minmax(0, 2fr) 1.25fr;
    grid-template-areas:
              "left-sidebar main main"
              "left-sidebar main main";
    gap: 0px 25px;
    height: calc(100vh - var(--header-height));
    width: 100vw;
    padding: 10px 0px;
    background-color: var(--main-background-color);
}

main > * {
    height: 100%;
    width: 100%;
}

.main {
    grid-area: main;
}

.bottombar {
    padding-top: 20px;
    grid-area: bottombar;
}

.left-sidebar {
    grid-area: left-sidebar;
}

.right-sidebar {
    grid-area: right-sidebar;
}
</style>