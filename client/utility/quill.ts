import Quill from 'quill';

function quill(node: HTMLElement, options) {
    const quill = new Quill(node, {
        modules: {
            toolbar: [
                [{ header: [1, 2, 3, false] }],
                ['bold', 'italic', 'underline', 'strike'],
                ['link', 'code-block']
            ]
        },
        placeholder: 'Type something...',
        theme: 'snow', // or 'bubble'
        bounds: node,
        ...options
    });
    const container = node.getElementsByClassName('ql-editor')[0];

    quill.on('text-change', function (delta, oldDelta, source) {
        node.dispatchEvent(
            new CustomEvent('text-change', {
                detail: {
                    html: container.innerHTML,
                    text: quill.getText()
                }
            })
        );
    });
}

export { quill };
