<script lang="ts">
import type { Realm, Update } from "../api/types";
import RealmOption from "./RealmOption.svelte";
import { fade, slide } from "svelte/transition";
import { flip } from "svelte/animate";
import SkeletonLayout from "../utility/components/SkeletonLayout.svelte";


export let realms: Realm[];
export let update: Update;

function selectRealm(realm: Realm) {
    update.realm_id = realm.id;
    update.realm_type = realm.realm_type;
}

</script>

<div class="realm-chooser">
    <h3>Choose a Destination for this Update</h3>
    <h4>Selected Realm</h4>
    {#key update.realm_id}
        <div class="selected-realm" in:fade>
            {#if update.realm_id }
                <RealmOption
                    realm={realms.find((realm) => realm.id === update.realm_id)}
                    on:click={() => selectRealm({ id: '', realm_type: '', name: ''})}
                    selected />
            {:else}
                <p style="font-style: italic;">No realm selected</p>
            {/if}
        </div>
    {/key}
    <h4>Realm List</h4>
    <div class="realm-list">
        {#each realms.filter((realm) => realm.id !== update.realm_id) as realm (realm.id)}
            <div
                animate:flip={{ delay: 200 }}
                in:fade={{ duration: 200 }}
                out:slide={{ duration: 200 }}>
                <RealmOption {realm} on:click={() => selectRealm(realm)} />
            </div>
        {:else}
            {#each new Array(10).fill(0) as _ }
                <SkeletonLayout>
                    <RealmOption realm={{ id: 'load', name: '_'.repeat(Math.random() * 10 + 5), realm_type: 'course'}} />
                </SkeletonLayout>
            {/each}
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
}

.realm-list {
    display: flex;
    flex-flow: column nowrap;
    max-height: 100%;
    padding: 0px 10px;
    overflow-y: auto;
}

h3, h4 {
    margin: 0px auto;
    text-align: center;
}
</style>