window.addEventListener('DOMContentLoaded', () => {

    //  Add Navbar Active Item
    
        const currentUrl = window.location.href;
        const navbarLinks = document.querySelectorAll('.navbar__link');
    
        navbarLinks.forEach((link) => {
            if (link.href === currentUrl) {
                link.parentNode.classList.add('active');
            }
        });
    });