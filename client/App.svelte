<script lang="ts" context="module">
declare const csrf_token: string;

export function getNewUpdate(): Update {
    return {
        id: -1,
        body: '',
        attachments: '',
        realm_id: '',
        realm_type: '',
        job: null,
    };
}
</script>

<script lang="ts">
import { onMount, tick } from 'svelte';
import type { Networking } from './api/network';
import * as networking from './api/network';
import type { Update } from './api/types';
import UpdateEditor from './editor/UpdateEditor.svelte';
import CardList from './layouts/CardList.svelte';
import Layout from './layouts/Layout.svelte';
import type { GridArea } from './layouts/Layout.svelte';
import Sidebar from './layouts/Sidebar.svelte';
import RealmChooser from './realms/RealmChooser.svelte';
import { realms, updates } from './stores';
import UpdateCard from './updates/UpdateCard.svelte';
import { fly, slide } from 'svelte/transition';
import { sleep } from './utility/async';

let layout: Layout | undefined;
let api: Networking | undefined;
let selectedUpdate: Update = getNewUpdate();

let scheduledUpdates = [] as Update[];
let savedUpdates = [] as Update[];
let rightSidebarTransitionDelay: number = 0;
let bottombarTransitionDelay: number = 0;
let gridAreas: GridArea = 'minimal';

$: {
    const _scheduledUpdates = $updates.filter(
        (update) => update.job?.scheduled_for || update.job?.scheduled_in
    );
    const _savedUpdates = $updates.filter(
        (update) => !(update.job?.scheduled_for || update.job?.scheduled_in)
    );

    let _gridAreas: GridArea;
    if (_scheduledUpdates.length === 0 && _savedUpdates.length == 0) {
        _gridAreas = 'minimal';
    } else if (_scheduledUpdates.length === 0) {
        _gridAreas = 'bottombar';
    } else if (_savedUpdates.length === 0) {
        _gridAreas = 'rightsidebar';
    } else {
        _gridAreas = 'maximum';
    }

    // Set transition delays before updating scheduled & saved updates so
    // the new delays can be used in subsequent transitions
    rightSidebarTransitionDelay = layout?.getElementTransitionDelay('right-sidebar', _gridAreas) ?? 0;
    bottombarTransitionDelay = layout?.getElementTransitionDelay('bottombar', _gridAreas) ?? 0;
    console.log('Rightbar delay:', rightSidebarTransitionDelay, 'Bottombar delay:', bottombarTransitionDelay);

    tick().then(() => {
        scheduledUpdates = _scheduledUpdates;
        savedUpdates = _savedUpdates;
        gridAreas = _gridAreas;
    });
}


onMount(() => {
    api = networking.mountNetworking(csrf_token);

    realms.setAPI(api);
    realms.reset();

    updates.setAPI(api);
    updates.reset();
});

function handleUpdateDelete(update: Update) {
    if (update.id === selectedUpdate.id) {
        selectedUpdate = getNewUpdate();
    }
}
</script>

<Layout areas={gridAreas} bind:this={layout}>
    <slot slot="main">
        <UpdateEditor bind:update={selectedUpdate} />
    </slot>
    <slot slot="bottombar">
        {#if savedUpdates.length !== 0}
            <div
                in:fly={{ y: 50, duration: 250, delay: bottombarTransitionDelay }}
                out:fly={{ y: 50, duration: 250, delay: bottombarTransitionDelay }}>
                <CardList
                    header={'Saved Updates'}
                    horizontal
                    items={savedUpdates}
                    let:item>
                    <UpdateCard
                        update={item}
                        selected={item === selectedUpdate}
                        on:edit={() => (selectedUpdate = item)}
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
                            selected={item === selectedUpdate}
                            update={item}
                            on:edit={() => (selectedUpdate = item)}
                            on:delete={() => handleUpdateDelete(item)} />
                    </CardList>
                </Sidebar>
            </div>
        {/if}
    </slot>
</Layout>

<style>
:root {
    --main-background-color: lightgray;
}
</style>
