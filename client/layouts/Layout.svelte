<script lang="ts">

</script>

<main>
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
    grid-template-columns: 1fr 3fr 1fr;
    grid-template-rows: minmax(0, 2fr) 1fr;
    grid-template-areas:
        "left-sidebar main right-sidebar"
        "left-sidebar bottombar right-sidebar";
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
    grid-area: bottombar;
}

.left-sidebar {
    grid-area: left-sidebar;
}

.right-sidebar {
    grid-area: right-sidebar;
}
</style>