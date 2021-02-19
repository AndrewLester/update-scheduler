<script lang="ts">
import Drawer, {Scrim} from '@smui/drawer/bare';
import '@smui/drawer/bare.css';
import IconButton, {Icon} from '@smui/icon-button/bare';
import '@smui/icon-button/bare.css';

export let open: boolean;
export let right = false;

</script>

<Drawer variant="modal" bind:open class="{right ? 'right': ''}" style="top: var(--header-height);">
    <div class="drawer-wrapper">
        <div class="icon-button-wrapper" class:right>
            <IconButton on:click={() => open = false}>
                <Icon class="material-icons">close</Icon>
            </IconButton>
        </div>
        <slot />
    </div>
</Drawer>
<Scrim />

<style>
.drawer-wrapper {
    width: 100%;
    height: 100%;
}

.icon-button-wrapper {
    position: absolute;
    top: 10px;
    right: 10px;
}

.icon-button-wrapper.right {
    right: 0px;
    left: 10px;
}

:global(.right.mdc-drawer--modal), :global(.right.mdc-drawer--modal){
left: initial;
right: 0;
}
:global(.right.mdc-drawer--animate), :global(.right.mdc-drawer--animate){
-webkit-transform: translateX(100%);
transform: translateX(100%);
}
:global(.right.mdc-drawer--opening), :global(.right.mdc-drawer--opening){
-webkit-transform: translateX(0);
transform: translateX(0);
}
:global(.right.mdc-drawer--closing), :global(.right.mdc-drawer--closing){
-webkit-transform: translateX(100%);
transform: translateX(100%);
}
</style>