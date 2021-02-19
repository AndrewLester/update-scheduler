import { svelteTransitionEnd } from "../utility/async";

type TransitionFunction = (original: HTMLElement, replacement: HTMLElement, duration: number) => Promise<void>;

export interface Transition {
    original: string,
    replacement: string,
    transitionFunction: TransitionFunction,
    duration: number
}

export async function leftSidebarTransition(original: HTMLElement, replacement: HTMLElement, duration: number) {
    original.style.display = 'none';
}

export async function bottomBarTransition(original: HTMLElement, replacement: HTMLElement, duration: number) {
    await dimensionPropertyTransition(original, replacement, duration, 'height');
}

export async function rightSidebarTransition(original: HTMLElement, replacement: HTMLElement, duration: number) {
    await dimensionPropertyTransition(original, replacement, duration, 'width');
}

export async function dimensionPropertyTransition(
    original: HTMLElement,
    replacement: HTMLElement,
    duration: number,
    dimensionProperty: string,
) {
    const titleCaseDimensionProperty = dimensionProperty.slice(0, 1).toUpperCase() + dimensionProperty.slice(1);
    const maxDimensionProperty = `max${titleCaseDimensionProperty}`;
    const clientDimensionProperty = `client${titleCaseDimensionProperty}`;

    replacement.style[dimensionProperty] = `calc(100% + ${original[clientDimensionProperty]}px)`;
    replacement.style.transition = `max-${dimensionProperty} ${duration}ms ease`;
    replacement.style[maxDimensionProperty] = `calc(100% + ${original[clientDimensionProperty]}px)`;
    if (original.firstElementChild) {
        await svelteTransitionEnd(original.firstElementChild, 5000);
    }

    replacement.style.transition = 'none';
    replacement.style[maxDimensionProperty] = '100%';
    // Use requestAnimationFrame to reset max-height property after
    // Max-height has transitioned to the right spot. This prevents a 
    // Reverse transition after the height is switched by the grid
    requestAnimationFrame(() => {
        replacement.style[maxDimensionProperty] = '';
        replacement.style[dimensionProperty] = '100%';
    });
}
