import type { Realm, Update } from "./api/types";
import { ListNetworkStore, ReadableNetworkStore } from "./utility/networkstore";


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

export { updates, realms };
