<script lang="ts">
import { onDestroy } from 'svelte';
import Layout from './layouts/Layout.svelte';
import UpdateEditor from './editor/UpdateEditor.svelte';
import Bottombar from './layouts/Bottombar.svelte';
import ScheduledUpdateList from './updates/ScheduledUpdateList.svelte';
import type { Update } from './api/types';
import Sidebar from './layouts/Sidebar.svelte';

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
        <ScheduledUpdateList scheduledUpdates={updates} />
    </slot>
    <slot slot="left-sidebar">
        <Sidebar side={'left'} />
    </slot>
    <slot slot="right-sidebar">
        <Sidebar side={'right'} />
    </slot>
</Layout>

<style>
:root {
    --main-background-color: lightgray;
}
</style>