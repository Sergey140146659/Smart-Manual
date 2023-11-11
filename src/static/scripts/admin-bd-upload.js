window.addEventListener('DOMContentLoaded', () => {

//  Post Request

    const postRequest = async (url, data = null) => {
        const res = await fetch(url, {
            method: "POST",
            headers: {
                'Content-type': 'application/json'
            },
            body: data
        });

        return await res.json();
    };


//  Get Request

    const getRequest = async (url) => {
        const response = await fetch(url, {
            method: 'GET'
        });
        return response.json();
    }


//  Get Cookie

    function getCookie() {
        return document.cookie.split('; ').reduce((acc, item) => {
            const [name, value] = item.split('=')
            acc[name] = value
            return acc
        }, {})
    }


//  Send Upload File Form

    const uploadForm = document.querySelector('.db-upload__form');
    const ansMessage = uploadForm.querySelector('.form__ans-message');
    const fileInput = uploadForm.querySelector('.form__db-file-input');

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        ansMessage.innerHTML = `
            <div class="loader-container form__loader-container">
                <span class="loader"></span>
            </div>
        `;

        const response = await fetch('/db/upload_db', {
            method: 'POST',
            body: formData
        })
        .then(data => {
            if (data.ok) {
                ansMessage.innerHTML = `
                    <span class="success_message">Успешно</span>
                `;
            } else {
                ansMessage.innerHTML = `
                    <span class="error_message">Ошибка</span>
                `;
            }
            fileInput.value = null;
        });
    });
});