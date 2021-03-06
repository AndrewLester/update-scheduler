export function sleep(millis: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, millis));
}

type AnimationEventListener = (ev: AnimationEvent) => any;

export function svelteTransitionEnd(
    element: Element,
    timeout?: number
): Promise<void> {
    return new Promise((resolve) => {
        element.addEventListener('outroend', () => resolve());

        if (timeout !== undefined) {
            sleep(timeout).then(() => {
                element.removeEventListener('outroend', () => resolve());
                resolve();
            });
        }
    });
}

export function animationEnd(
    element: Element,
    animationName: string,
    timeout?: number
): Promise<void> {
    return new Promise((resolve) => {
        const callback: AnimationEventListener = (e) => {
            const svelteClassNameBase = element.className
                .split(' ')
                .filter((className) => className.startsWith('svelte'));

            const baseAnimationName = svelteClassNameBase
                ? svelteClassNameBase[0] + '-'
                : '';

            if (e.animationName === baseAnimationName + animationName) {
                element.removeEventListener('animationend', callback);
                resolve();
            }
        };
        element.addEventListener('animationend', callback);

        if (timeout !== undefined) {
            sleep(timeout).then(() => {
                element.removeEventListener('animationend', callback);
                resolve();
            });
        }
    });
}