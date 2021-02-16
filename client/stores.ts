import { readable, writable } from "svelte/store";
import type { Realm, Update } from "./api/types";
import { ListNetworkStore, ReadableNetworkStore } from "./utility/networkstore";
import moment, { Moment } from 'moment';
import * as notifier from './notifications/notifier';


function errorHandler(error: object | string, _) {
    if (typeof error === 'string' || 'message' in error) {
        notifier.danger(typeof error === 'object' ? (error as any).message : error, 2000);
    } else if ('errors' in error) {
        notifier.danger('One or more required fields were missing', 2000);
    } else {
        notifier.danger('An error occured', 2000);
    }
}


const updates = new ListNetworkStore<Update[]>(
    '/scheduler/updates',
    [],
    errorHandler
);

const realms = new ReadableNetworkStore<Realm[]>(
    '/scheduler/realms',
    [],
    errorHandler
);

const time = readable<Moment>(moment(), (set) => {
    const interval = setInterval(() => {
        set(moment());
    }, 1000);
    return () => clearInterval(interval);
});

const selectedUpdate = writable<Update>(getNewUpdate());

export { updates, realms, time, selectedUpdate };
