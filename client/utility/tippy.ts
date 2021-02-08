import type { destroy_block } from 'svelte/internal';
import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';

export default function(node: HTMLElement, props: object) {
    tippy(node, props);

    return {
        update(newProps: object) {
            (node as any)._tippy.setProps(newProps);
        },
        destroy() {
            (node as any)._tippy.destroy();
        }
    };
}