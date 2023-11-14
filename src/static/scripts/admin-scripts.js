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