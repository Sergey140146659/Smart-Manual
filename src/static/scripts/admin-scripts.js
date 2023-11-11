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


//  Logout

    const logoutButton = document.getElementById('logout_button');

    logoutButton.addEventListener('click', (event) => {
        event.preventDefault();

        postRequest('/auth/logout')
        .then(data => {
            console.log('success');
            window.location.href = '/pages/login';
        }).catch(() => {
            console.log('error');
            window.location.href = '/pages/login';
        }).finally(() => {
            form.reset();
        });
    });


//  Dropdown

    let dropdownList = document.querySelectorAll('.dropdown');

    dropdownList.forEach(dropdown => {
        const dropdownContent = dropdown.querySelector('.dropdown__content');

        dropdown.addEventListener("mouseenter", () => {
            dropdownContent.classList.remove('d-none');
        });
        dropdownContent.addEventListener("mouseenter", () => {
            dropdownContent.classList.remove('d-none');
        });

        dropdown.addEventListener("mouseleave", () => {
            dropdownContent.classList.add('d-none');
        });
    });


//  Add Navbar Active Item

    const currentUrl = window.location.href;
    const navbarLinks = document.querySelectorAll('.navbar__link');

    navbarLinks.forEach((link) => {
        if (link.href === currentUrl) {
            link.parentNode.classList.add('active');
        }

        if (currentUrl === 'http://localhost:8000/pages/admin_bot_rate' ||
            currentUrl === 'http://localhost:8000/pages/admin_rates') {
                const dropdown = document.querySelector('.navbar__item.dropdown');
                dropdown.classList.add('active');
            }
    });
});