import Quill from 'quill';
import ImageCompress from 'quill-image-compress';

Quill.register('modules/imageCompress', ImageCompress);

function quill(node: HTMLElement, options = {}) {
    const quill = new Quill(node, {
        modules: {
            toolbar: [
                [{ header: [1, 2, 3, false] }],
                ['bold', 'italic', 'underline', 'strike'],
                [{ color: [] }, { background: [] }],
                [{ list: 'ordered' }, { list: 'bullet' }],
                ['link', 'image', 'video'],
            ],
            imageCompress: {
                quality: 0.9,
                maxWidth: 500,
                maxHeight: 500,
                ignoreImageTypes: [],
                keepImageTypes: [],
                imageType: 'image/jpeg',
            },
        },
        placeholder: 'Type something...',
        theme: 'snow',
        bounds: node,
        ...options,
    });
    const container = node.getElementsByClassName('ql-editor')[0];

    quill.on('text-change', function (delta, oldDelta, source) {
        node.dispatchEvent(
            new CustomEvent('text-change', {
                detail: {
                    html: container.innerHTML,
                    text: quill.getText(),
                },
            })
        );
    });
}

export { quill };
