window.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');

    const postLogin = async (url, data) => {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-type': 'application/json'
            },
            body: data,
        });
        return response.json();
    }


    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        const postJson = JSON.stringify({
            'email': formData.get('email'),
            'password': formData.get('password')
        });

        postLogin('/auth/login', postJson)
        .then(data => {
            if (data.status && data.status == 'success') {
                console.log('success');
                window.location.href = '/pages/admin_bot_rate';
            }
        }).catch(() => {
            console.log('error');
        }).finally(() => {
            form.reset();
        });
    });
});