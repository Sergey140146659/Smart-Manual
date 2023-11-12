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


let subjectTargetName = '';

//  Add Subject Form

    const subjectFormDOM = document.querySelector(".add-subject-form");
    subjectFormDOM.addEventListener('submit', (e) => {
        e.preventDefault();
        const subjectNameInput = document.querySelector('.subject-form__input');
        const newSubjectName = subjectNameInput.value;

        createSubjectDOM(newSubjectName);
        subjectNameInput.value = '';
    });

    function createSubjectDOM (subjectName) {
        const subjectsList = document.querySelector('.loaded-db__list');

        const newSubject = document.createElement('li');
        newSubject.classList.add('loaded-db__item');
        newSubject.innerHTML = `
            <button type="button" class="loaded-db__item__button">${subjectName}</button>
        `;
        subjectsList.append(newSubject);
        chooseSubject(newSubject.querySelector('button'));
    }


//  Choose Subject

    function chooseSubject (subjectButtonDOM) {
        clearSubjectsActiveButton();
        subjectButtonDOM.classList.add('active');
        subjectTargetName = subjectButtonDOM.textContent;
    }

    function clearSubjectsActiveButton () {
        const activeButton = document.querySelector('.loaded-db__item__button.active');
        if (activeButton) {
            activeButton.classList.remove('active');
        }
    }
});