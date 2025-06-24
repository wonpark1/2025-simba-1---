document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById('delete-image-btn');
    const flag = document.getElementById('delete_image_field');
    const fileInput = document.querySelector('input[name="image"]');
    let wrap = document.getElementById('current-image-wrapper');

    if (button && flag) {
        button.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();
            flag.value = 'true';
            if (wrap) {
                wrap.remove();
                wrap = null;
            }
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            if (flag) flag.value = 'false';

            const read = new FileReader();
            read.onload = ev => {
                const imageURL = ev.target.result;

                if (!wrap) {
                    wrap = document.createElement('div');
                    wrap.id = 'current-image-wrapper';
                    wrap.classList.add('image-wrapper');

                    const del_button = document.createElement('button');
                    del_button.id = 'delete-image-btn';
                    del_button.type = 'button';
                    del_button.className = 'delete-image-btn';
                    del_button.innerHTML = `<img id="x" src="{% static 'icons/x.svg' %}" height="13" width="13" alt="x">`;
                    wrap.appendChild(del_button);

                    del_button.addEventListener('click', Evt => {
                        Evt.preventDefault();
                        Evt.stopPropagation();
                        flag.value = 'true';
                        if (wrap) wrap.remove();
                        wrap = null;
                        fileInput.value = '';
                    });

                    const container2 = document.querySelector('.container2');
                    container2.prepend(wrap);
                }

                let ImageTag = wrap.querySelector('img.image');
                if (!ImageTag) {
                    ImageTag = document.createElement('img');
                    ImageTag.className = 'image';
                    wrap.prepend(ImageTag);
                }
                ImageTag.src = imageURL;
            };
            read.readAsDataURL(file);
        });
    }
});