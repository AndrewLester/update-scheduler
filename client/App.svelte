<script lang="ts">
import { onDestroy } from 'svelte';
import Layout from './layouts/Layout.svelte';
import UpdateEditor from './editor/UpdateEditor.svelte';
import Bottombar from './layouts/Bottombar.svelte';
import ScheduledUpdateList from './updates/ScheduledUpdateList.svelte';
import type { Update } from './api/types';
import Sidebar from './layouts/Sidebar.svelte';
import CardList from './layouts/CardList.svelte';
import UpdateCard from './updates/UpdateCard.svelte';

const updates: Update[] = [
    {
        id: -1,
        realm_type: 'group',
        realm_id: '35353',
        attachments: '',
        body: 'hi',
        job: {
            id: 4,
            scheduled_at: '252',
            scheduled_for: '552'
        }
    }
]
</script>

<Layout>
    <slot slot="main">
        <UpdateEditor />
    </slot>
    <slot slot="bottombar">
        <CardList header={'Saved Updates'} horizontal items={updates} let:item>
            <UpdateCard update={item} />
        </CardList>
    </slot>
    <slot slot="left-sidebar">
        <Sidebar side={'left'} />
    </slot>
    <slot slot="right-sidebar">
        <Sidebar side={'right'}>
            <CardList header={'Scheduled Updates'} items={updates} let:item>
                <UpdateCard update={item} />
            </CardList>
        </Sidebar>
    </slot>
</Layout>

<style>
:root {
    --main-background-color: lightgray;
}
</style>