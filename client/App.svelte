<script lang="ts" context="module">
declare const csrf_token: string;

export function getNewUpdate(): Update {
    return { id: -1, body: '', attachments: '', realm_id: 0, realm_type: '', job: null };
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


let api: Networking | undefined;
let selectedUpdate: Update = getNewUpdate();

$: scheduledUpdates = $updates.filter((update) => update.job);
$: savedUpdates = $updates.filter((update) => !update.job);
let gridAreas: GridArea = 'minimal';
$: if (scheduledUpdates || savedUpdates || true) {
    console.time('layout-change');
}
$: {
    if (scheduledUpdates.length === 0 && savedUpdates.length == 0) {
        gridAreas = 'minimal';
    } else if (scheduledUpdates.length === 0) {
        gridAreas = 'bottombar';
    } else if (savedUpdates.length === 0) {
        gridAreas = 'rightsidebar';
    } else {
        gridAreas = 'maximum';
    }
    console.timeLog('layout-change', 'Areas updated in App.svelte');
};

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

<Layout areas={gridAreas}>
    <slot slot="main">
        <UpdateEditor bind:update={selectedUpdate} />
    </slot>
    <slot slot="bottombar">
        {#if savedUpdates.length !== 0 }
            <div transition:fly={{ y: 50, duration: 250 }}
                on:outrostart={() => console.timeLog('layout-change', 'Fly animation start')}
                on:outroend={() => {console.timeLog('layout-change', 'Fly animation done')}}>
                <CardList header={'Saved Updates'} horizontal items={savedUpdates} let:item>
                    <UpdateCard
                        update={item}
                        selected={item === selectedUpdate}
                        on:edit={() => selectedUpdate = item}
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
        {#if scheduledUpdates.length !== 0 }
            <div transition:fly={{ x: 50, duration: 250 }}>
                <Sidebar side={'right'}>
                    <CardList header={'Scheduled Updates'} items={scheduledUpdates} let:item>
                        <UpdateCard
                        selected={item === selectedUpdate}
                        update={item}
                        on:edit={() => selectedUpdate = item}
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