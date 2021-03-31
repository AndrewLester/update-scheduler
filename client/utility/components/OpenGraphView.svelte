<script lang="ts">
import { slide } from 'svelte/transition';
import type { TransitionConfig } from 'svelte/transition';
import { Icon } from '@smui/button/bare';
import '@smui/button/bare.css';

export let data: any;
export let alternativeIcon: string = 'link';
export let transition: (node: Element, params: object) => TransitionConfig = slide;

let iconFailed = false;

</script>

<div class="open-graph-wrapper">
    <a href="{data.url}" title="Attachment preview"
        style="color: black;" target="_blank">
        <div class="open-graph-preview" transition:transition|local>
            {#if data.image}
                <img class="open-graph-image" src="{data.image}" alt="{data.title} image">
            {:else}
                <div class="open-graph-icon">
                    {#if data.icon && !iconFailed}
                        <img src="{data.icon}" alt="{data.title} icon" on:error={() => iconFailed = true}>
                    {:else}
                        <Icon class="material-icons">{alternativeIcon}</Icon>
                    {/if}
                </div>
            {/if}
            <div class="open-graph-text">
                <h3>{data.title}</h3>
                <p  class="description"
                    class:no-data={!data.description}>
                    {data.description || 'No description'}</p>
                <p class="url">{data.url}</p>
            </div>
        </div>
    </a>
</div>

<style>
.open-graph-wrapper {
    flex: 1 1 auto;
    overflow: hidden;
}
.open-graph-preview {
    display: flex;
    flex-flow: row nowrap;
    gap: 0px 10px;
    border: 1px solid gray;
    border-radius: 5px;
    height: 120px;
    overflow: hidden;
}
.open-graph-text {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    overflow: hidden;
    color: black;
}
.open-graph-text > * {
    flex: 0 1 auto;
    overflow: hidden;
}
.open-graph-text h3 {
    margin: 5px 0px;
    font-weight: bold;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 0 0 auto;
}
.open-graph-text .description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}
.open-graph-text .url {
    color: gray;
    font-size: 12px;
    margin-top: auto;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 0 0 auto;
}
.open-graph-image {
    width: 120px;
    height: 120px;
    flex: 0 0 auto;
}
.open-graph-icon {
    display: flex;
    flex-flow: row nowrap;
    flex: 0 0 auto;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    background-color: lightgray;
}
.open-graph-icon :global(*) {
    text-decoration: none;
}
.open-graph-icon > :global(*) {
    font-size: 30px;
}
.open-graph-icon > img {
    width: 60px;
    height: 60px;
}
.open-graph-preview .no-data {
    font-style: italic;
}
@media (max-width: 1050px) {
    .open-graph-preview {
        height: 65px;
    }
    .open-graph-icon {
        height: 65px;
        width: 65px;
    }
    .open-graph-text h3 {
        font-size: 15px;
    }
    .open-graph-text .url {
        background: transparent;
    }
    .open-graph-image {
        width: 65px;
        height: 65px;
    }
    .open-graph-icon > img {
        width: 30px;
        height: 30px;
    }
    .open-graph-icon > :global(*) {
        font-size: 18px;
    }
    .open-graph-text .description {
        -webkit-line-clamp: 1;
    }
}
</style>