<script lang="ts" context="module">
declare const bootstrap: {
    csrf_token: string;
    timezone: string;
};
</script>

<script lang="ts">
import { onMount, setContext, tick } from 'svelte';
import type { Networking } from './api/network';
import * as networking from './api/network';
import type { Update } from './api/types';
import { getNewUpdate, isScheduled } from './api/types';
import UpdateEditor from './editor/UpdateEditor.svelte';
import CardList from './layouts/CardList.svelte';
import Layout from './layouts/Layout.svelte';
import type { GridArea } from './layouts/Layout.svelte';
import Sidebar from './layouts/Sidebar.svelte';
import RealmChooser from './realms/RealmChooser.svelte';
import { realms, updates } from './stores';
import UpdateCard from './updates/UpdateCard.svelte';
import { fly } from 'svelte/transition';
import NotificationDisplay from './notifications/NotificationDisplay.svelte';
import NavigationDrawer from './utility/components/NavigationDrawer.svelte';
import IconButton, { Icon } from '@smui/icon-button/bare';
import '@smui/icon-button/bare.css';

let layout: Layout | undefined;
let api: Networking | undefined;
let selectedUpdate: Update = getNewUpdate();
let screenWidth: number | undefined;

setContext('mobile', () => mobile);

// TODO: Make mobile reactive after allowing layout to change from
// mobile to normal using transitions. Remove it from onMount
let mobile = false;
$: scheduledUpdates = $updates.filter((update) => isScheduled(update));
$: savedUpdates = $updates.filter((update) => !isScheduled(update));

let gridAreas: GridArea = 'minimal';
let realmDrawerOpen = false;
let updateDrawerOpen = false;

$: {
    if (mobile) {
        gridAreas = 'mobile';
    } else if (scheduledUpdates.length === 0 && savedUpdates.length == 0) {
        gridAreas = 'minimal';
    } else if (scheduledUpdates.length === 0) {
        gridAreas = 'bottombar';
    } else if (savedUpdates.length === 0) {
        gridAreas = 'rightsidebar';
    } else {
        gridAreas = 'maximum';
    }
}

$: rightSidebarTransitionDelay = layout
    ? layout.getElementTransitionDelay('right-sidebar', gridAreas) || 0
    : 0;
$: bottombarTransitionDelay = layout
    ? layout.getElementTransitionDelay('bottombar', gridAreas) || 0
    : 0;

onMount(() => {
    api = networking.mountNetworking(bootstrap.csrf_token);

    realms.setAPI(api);
    realms.reset();

    updates.setAPI(api);
    updates.reset();

    mobile = !!screenWidth && screenWidth < 1050;
});

function handleUpdateEdit(update: Update) {
    selectedUpdate = JSON.parse(JSON.stringify(update));
    updateDrawerOpen = false;
    realmDrawerOpen = false;
}

function handleUpdateDelete(update: Update) {
    if (update.id === selectedUpdate.id) {
        selectedUpdate = getNewUpdate();
    }
}

function handleUpdateCancel(update: Update) {
    handleUpdateDelete(update);
}
</script>

<svelte:window bind:innerWidth={screenWidth} />

<Layout areas={gridAreas} bind:this={layout}>
    <slot slot="main">
        {#if mobile}
            <div class="mobile-drawer-buttons">
                <IconButton
                    on:click={() => (realmDrawerOpen = !realmDrawerOpen)}>
                    <Icon class="material-icons">group</Icon>
                </IconButton>
                <IconButton
                    on:click={() => (updateDrawerOpen = !updateDrawerOpen)}>
                    <Icon class="material-icons">schedule_send</Icon>
                </IconButton>
            </div>
        {/if}
        <UpdateEditor bind:update={selectedUpdate} />
    </slot>
    <slot slot="bottombar">
        {#if savedUpdates.length !== 0}
            <!-- Must use separate in and out transitions because delay parameter is dynamic -->
            <div
                in:fly={{ y: 50, duration: 300, delay: bottombarTransitionDelay }}
                out:fly={{ y: 50, duration: 300, delay: bottombarTransitionDelay }}>
                <CardList
                    header={'Saved Updates'}
                    horizontal
                    items={savedUpdates}
                    let:item>
                    <UpdateCard
                        update={item}
                        selected={item.id === selectedUpdate.id}
                        on:edit={() => handleUpdateEdit(item)}
                        on:delete={() => handleUpdateDelete(item)} />
                </CardList>
            </div>
        {/if}
    </slot>
    <slot slot="left-sidebar">
        <Sidebar side={'left'}>
            <RealmChooser bind:update={selectedUpdate} realms={$realms} />
        </Sidebar>
    </slot>
    <slot slot="right-sidebar">
        {#if scheduledUpdates.length !== 0}
            <!-- Must use separate in and out transitions because delay parameter is dynamic -->
            <div
                in:fly={{ x: 50, duration: 250, delay: rightSidebarTransitionDelay }}
                out:fly={{ x: 100, duration: 250, delay: rightSidebarTransitionDelay }}
                style="height: 100%;">
                <Sidebar side={'right'}>
                    <CardList
                        header={'Scheduled Updates'}
                        items={scheduledUpdates}
                        let:item>
                        <UpdateCard
                            selected={item.id === selectedUpdate.id}
                            update={item}
                            on:edit={() => handleUpdateEdit(item)}
                            on:cancel={() => handleUpdateCancel(item)} />
                    </CardList>
                </Sidebar>
            </div>
        {/if}
    </slot>

    <slot slot="drawer">
        {#if mobile}
            <NavigationDrawer bind:open={realmDrawerOpen}>
                <RealmChooser bind:update={selectedUpdate} realms={$realms} />
            </NavigationDrawer>
            <NavigationDrawer bind:open={updateDrawerOpen} right>
                <div style="display: flex; flex-direction: column;">
                    <CardList
                        header={'Saved Updates'}
                        horizontal
                        items={savedUpdates}
                        let:item>
                        <UpdateCard
                            update={item}
                            selected={item.id === selectedUpdate.id}
                            on:edit={() => handleUpdateEdit(item)}
                            on:delete={() => handleUpdateDelete(item)} />
                    </CardList>
                    <CardList
                        header={'Scheduled Updates'}
                        horizontal
                        items={scheduledUpdates}
                        let:item>
                        <UpdateCard
                            selected={item.id === selectedUpdate.id}
                            update={item}
                            on:edit={() => handleUpdateEdit(item)}
                            on:delete={() => handleUpdateDelete(item)} />
                    </CardList>
                </div>
            </NavigationDrawer>
        {/if}
    </slot>
</Layout>
<NotificationDisplay options={{ timeout: 2500, width: '200px' }} />

<style>
:root {
    --main-background-color: lightgray;
    --mdc-theme-primary: #29b6f6;
}

.mobile-drawer-buttons {
    position: absolute;
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    width: 100%;
}
</style>
