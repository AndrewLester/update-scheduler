<script lang="ts">
import Checkbox from '@smui/checkbox/bare.js';
import '@smui/checkbox/bare.css';
import type { Realm } from '../api/types';
import { slide } from 'svelte/transition';

export let realm: Realm;
export let selected: boolean;

</script>

<div class="realm-option">
    <div class="realm-image" data-realm={realm.realm_type}></div>
    <p>{realm.name}</p>
    <div class="checkbox-wrapper">
        <Checkbox on:click checked={selected} />
    </div>
</div>

<style>
.realm-option {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    text-align: left;
}

.realm-image {
    flex: 0 0 auto;
    background: url('https://app.schoology.com/sites/all/themes/schoology_theme/images/icons_sprite_realm.png?5d0d37111b9f09da')
        no-repeat right;
    height: 20px;
    align-self: center;
    width: 30px;
    margin: 0px;
}

p {
    display: -webkit-box;
    text-overflow: ellipsis;
    overflow: hidden;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.checkbox-wrapper {
    margin-left: auto;
}

.realm-option > :last-child {
    margin-left: auto;
}

.realm-image[data-realm='section'] {
    background-position-y: -29px;
}

.realm-image[data-realm='group'] {
    background-position-y: -59px;
}

.realm-image[data-realm='user'] {
    background-position-y: -179px;
}

.realm-image[data-realm='school'] {
    background-position-y: -209px;
}
.realm-image[data-realm='district'] {
    width: 27px;
    background-position-y: -209px;
    background-repeat: repeat-x;
    background-position-x: 15px;
    margin-right: 3px;
}
</style>