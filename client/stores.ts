import { readable } from "svelte/store";
import type { Realm, Update } from "./api/types";
import { ListNetworkStore, ReadableNetworkStore } from "./utility/networkstore";
import moment, { Moment } from 'moment';
import * as notifier from './notifications/notifier';


function errorHandler(error: Error, _) {
    try {
        const json = JSON.parse(error.message);
        const errors = json.errors;

        if (typeof errors === 'string') {
            notifier.danger('An error occured. Try refreshing the page.');
            return;
        }

        notifier.danger('Missing required fields: ' + Object.keys(errors).join(', '), 2000);
        return;
    } catch (e) { }

    notifier.danger('An error occured. Check your update\'s post time.', 2000);
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

export { updates, realms, time };
