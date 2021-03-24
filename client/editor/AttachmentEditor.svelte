<script lang="ts">
import Tab, {Icon as TabIcon, Label as TabLabel} from '@smui/tab';
import TabBar from '@smui/tab-bar';
import '@smui/tab-bar/bare.css';
import '@smui/tab-indicator/bare.css';
import '@smui/tab-scroller/bare.css';
import '@smui/tab/bare.css';
import Button, { Label, Icon } from '@smui/button/bare';
import '@smui/button/bare.css';
import type { Attachment } from '../api/types';
import Textfield from '@smui/textfield/bare';
import '@smui/textfield/bare.css';
import { createEventDispatcher } from 'svelte';
import { getMetadata } from 'page-metadata-parser';
import OpenGraphView from '../utility/components/OpenGraphView.svelte';
import * as notifier from '../notifications/notifier';


export let attachment: Attachment;

const dispatch = createEventDispatcher();

const tabs = [
    {
        icon: 'link',
        label: 'link'
    },
    {
        icon: 'videocam',
        label: 'video'
    }
];

const urlRegex = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/;
let openGraphData: any;
let active = tabs.find((tab) => tab.label === attachment.type) || tabs[0];
$: attachment.type = active.label as 'video' | 'link' | 'file';
$: {
    const matches = attachment.url.match(urlRegex);
    if (attachment.url && attachment.url.includes('.')
        && matches !== null && matches.length >= 1
        && matches[0] === attachment.url) {
        fetch('/cors/' + attachment.url)
            .then((res) => {
                if (res.status >= 500) {
                    openGraphData = undefined;
                    throw new Error('Invalid URL/page request');
                }
                return res;
            })
            .then((res) => res.text())
            .then((html) => {
                const document = new DOMParser().parseFromString(html, 'text/html');
                const addSchema = !(attachment.url.startsWith('http://') || attachment.url.startsWith('https://'));
                const pageData = getMetadata(document, (addSchema ? 'http://' : '') + attachment.url);
                if (pageData.title) {
                    openGraphData = pageData;
                    attachment.title = openGraphData.title;
                    attachment.image = openGraphData.image;
                    attachment.icon = openGraphData.icon;
                    attachment.summary = openGraphData.description;
                } else {
                    openGraphData = undefined;
                }
            })
            .catch();
    } else {
        openGraphData = undefined;
    }
}

function save() {
    // TODO: Require certain fields
    const matches = attachment.url.match(urlRegex);
    if (!attachment.url || !attachment.url.includes('.') || !matches || matches[0] !== attachment.url) {
        notifier.danger('Please use a valid URL for your attachment.', 2500);
        return;
    }
    const addSchema = !(attachment.url.startsWith('http://') || attachment.url.startsWith('https://'));
    attachment.url = (addSchema ? 'http://' : '') + attachment.url;

    dispatch('save');
}
</script>

<div class="attachment-editor">
    <TabBar {tabs} let:tab bind:active style="width: 100%;">
        <Tab {tab}>
            <TabIcon class="material-icons">{tab.icon}</TabIcon>
            <TabLabel>{tab.label}</TabLabel>
        </Tab>
    </TabBar>
    {#if active.label === 'link'}
        <Textfield withLeadingIcon label="Enter a URL" bind:value={attachment.url}><Icon class="material-icons">link</Icon></Textfield>
    {:else if active.label === 'video'}
        <Textfield withLeadingIcon label="Enter a URL" bind:value={attachment.url}><Icon class="material-icons">videocam</Icon></Textfield>
    {/if}
    {#if openGraphData}
        <OpenGraphView data={openGraphData} alternativeIcon={active.icon} />
    {/if}
    <div class="button-row">
        <Button variant="outlined" on:click={() => dispatch('discard')}>
            <Label>Discard Edits</Label>
        </Button>
        <Button variant="outlined" on:click={save}>
            <Label>Save</Label>
        </Button>
    </div>
</div>

<style>
.button-row {
    margin-top: 20px;
}
</style>
