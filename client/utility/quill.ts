import Quill from 'quill';
import ImageCompress from 'quill-image-compress';
import ResizeModule from '@botom/quill-resize-module';

Quill.register('modules/resize', ResizeModule);
Quill.register('modules/imageCompress', ImageCompress);

const icons = Quill.import('ui/icons');
icons['video'] =
    '<svg xmlns="http://www.w3.org/2000/svg" height="18" width="18" viewBox="0 0 48 48"><path stroke-width="2" stroke="black" d="m16 35.9-12-12 12.1-12.1 2.15 2.15L8.3 23.9l9.85 9.85Zm15.9.1-2.15-2.15 9.95-9.95-9.85-9.85L32 11.9l12 12Z"/></svg>';

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
            resize: {
                locale: {},
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
