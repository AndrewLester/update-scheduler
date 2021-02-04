import { readable } from "svelte/store";
import type { Realm, Update } from "./api/types";
import { ListNetworkStore, ReadableNetworkStore } from "./utility/networkstore";
import moment, { Moment } from 'moment';


const updates = new ListNetworkStore<Update[]>(
    '/scheduler/updates',
    [],
    (error, _) => console.log(error)
);

const realms = new ReadableNetworkStore<Realm[]>(
    '/scheduler/realms',
    [],
    (error, _) => console.log(error)
);

const time = readable<Moment>(moment(), (set) => {
    const interval = setInterval(() => {
        set(moment());
    }, 1000);
    return () => clearInterval(interval);
});

export { updates, realms, time };
