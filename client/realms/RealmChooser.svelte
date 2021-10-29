<script lang="ts">
import type { Realm, Update } from '../api/types';
import RealmOption from './RealmOption.svelte';
import { fade, slide } from 'svelte/transition';
import { flip } from 'svelte/animate';
import Icon from '@smui/textfield/icon/index';
import Textfield from '@smui/textfield/bare';
import '@smui/textfield/bare.css';
import SkeletonLayout from '../utility/components/SkeletonLayout.svelte';
import { sleep } from '../utility/async';

export let realms: Realm[];
export let update: Update;

let search = '';
let searchInput = '';
$: (async () => {
    await sleep(50);
    search = searchInput;
})();

$: updateRealmIds = update.realms.map((realm) => realm.id);
$: availableRealms = realms.filter(
    (realm) =>
        !updateRealmIds.includes(realm.id) &&
        realm.name.toUpperCase().includes(search.toUpperCase())
);

function selectRealm(realm: Realm) {
    update.realms = [...update.realms, realm];

    searchInput = '';
}

function deselectRealm(realm: Realm) {
    update.realms = update.realms.filter(
        (existingRealm) => existingRealm.id !== realm.id
    );
}
</script>

<div class="realm-chooser">
    <h3>Choose a Destination for this Update</h3>
    <h4>Selected Realms</h4>
    <div class="selected-realms">
        {#each update.realms as realm (realm.id)}
            <div
                out:slide={{ duration: update.realms.length > 0 ? 200 : 0 }}
                in:slide={{ duration: 200 }}>
                <RealmOption
                    {realm}
                    on:click={() => deselectRealm(realm)}
                    selected />
            </div>
        {:else}
            <p
                style="font-style: italic; text-align: center;"
                in:fade={{ duration: 200 }}>
                No realms selected
            </p>
        {/each}
    </div>
    <h4 style="margin-top: 10px;">Realm List</h4>
    <div>
        <Textfield label="Search" withLeadingIcon bind:value={searchInput}>
            <Icon class="material-icons">search</Icon>
        </Textfield>
    </div>
    <div class="realm-list">
        {#each availableRealms as realm (realm.id)}
            <div
                animate:flip={{ duration: 200 }}
                transition:slide={{ duration: 200 }}>
                <RealmOption {realm} on:click={() => selectRealm(realm)} />
            </div>
        {:else}
            {#if realms.length !== 0}
                <div
                    style="margin-top: 10px; text-align: center; font-style: italic">
                    No realms found
                </div>
            {:else}
                {#each new Array(6).fill(0) as _}
                    <SkeletonLayout>
                        <RealmOption
                            realm={{ id: 'load', name: '_'.repeat(Math.random() * 15 + 7), type: 'course' }}
                            disabled />
                    </SkeletonLayout>
                {/each}
            {/if}
        {/each}
    </div>
</div>

<style>
.realm-chooser {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: 20px 10px;
    padding-bottom: 0px;
}

.realm-list {
    position: relative;
    display: flex;
    flex-flow: column nowrap;
    max-height: 100%;
    min-height: 80px;
    width: 100%;
    padding: 0px 10px;
    overflow-y: auto;
}

.selected-realms {
    height: auto;
    width: 80%;
}

.selected-realms > * {
    vertical-align: middle;
}

h3,
h4 {
    margin: 0px auto;
    text-align: center;
}

h4 {
    margin: 5px auto;
    font-weight: bold;
}
</style>
