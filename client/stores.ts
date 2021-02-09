import { readable } from "svelte/store";
import type { Realm, Update } from "./api/types";
import { ListNetworkStore, ReadableNetworkStore } from "./utility/networkstore";
import moment, { Moment } from 'moment';
import * as notifier from './notifications/notifier';


const updates = new ListNetworkStore<Update[]>(
    '/scheduler/updates',
    [],
    (error, _) => notifier.danger(error.message, 2000)
);

const realms = new ReadableNetworkStore<Realm[]>(
    '/scheduler/realms',
    [],
    (error, _) => notifier.danger(error.message, 2000)
);

const time = readable<Moment>(moment(), (set) => {
    const interval = setInterval(() => {
        set(moment());
    }, 1000);
    return () => clearInterval(interval);
});

export { updates, realms, time };
