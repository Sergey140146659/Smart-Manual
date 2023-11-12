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


// Subject Add Form

    const subjectFormDOM = document.querySelector(".add-subject-form");
    subjectFormDOM.addEventListener('submit', (e) => {
        e.preventDefault();
        const subjectNameInput = document.querySelector('.subject-form__input');
        const newSubjectName = subjectNameInput.value;

        const subjectItemDOM = createSubjectDOM(newSubjectName);
        chooseSubject(subjectItemDOM.querySelector('button'));
        subjectNameInput.value = '';
    });

    function createSubjectDOM (subjectName) {
        const subjectsListDOM = document.querySelector('.loaded-db__list');

        const newSubject = document.createElement('li');
        newSubject.classList.add('loaded-db__item');
        newSubject.innerHTML = `
            <button type="button" class="loaded-db__item__button">${subjectName}</button>
        `;
        subjectsListDOM.append(newSubject);
        return newSubject;
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


//  Send Subject Form

    const subjectFormDOM = document.querySelector('.subject-form');
    subjectFormDOM.addEventListener('submit', async (e) => {
        e.preventDefault();

    });


//  Get Subject List

    async function getSubjectList () {
        const subjectsList = await getRequest('../db/subject_list');
        clearSubjectListDOM();
        buildSubjectListDOM(subjectsList);
    }
    getSubjectList();

    function buildSubjectListDOM (subjectList) {
        for (subjectName of subjectList) {
            createSubjectDOM(subjectName);
        }
    }

    function clearSubjectListDOM () {
        const subjectListDOM = document.querySelector('.loaded-db__list');
        subjectListDOM.innerHTML = '';
    }


//  Add Theme DOM

    const addThemeButton = document.querySelector('.subject__add-theme-button');
    addThemeButton.addEventListener('click', () => {
        const subjectFormDOM = document.querySelector('.subject-form');
        const buttonsGroup = document.querySelector('.subject__buttons-group');
        const themeInputsGroup = document.createElement('div');
        themeInputsGroup.classList.add('theme-inputs-group');
        themeInputsGroup.innerHTML = `
            <label class="d-none" for="theme">Название темы</label>
            <input class="subject-form__input" type="text" id="theme" name="theme" placeholder="Название темы" autocomplete="off">
            <div class="number-inputs">
                <label class="d-none" for="start-page-num">Первая страница</label>
                <input class="subject-form__input page-num__input" type="number" id="start-page-num" name="start-page-num" placeholder="12" autocomplete="off">
                <span class="page-num__dash">—</span>
                <label class="d-none" for="end-page-num">Последняя страница</label>
                <input class="subject-form__input page-num__input" type="number" id="end-page-num" name="end-page-num" placeholder="16" autocomplete="off">
            </div>
            <button type="button" class="theme__delete-button">✕</button>
        `;
        const deleteButtonDOM = themeInputsGroup.querySelector('.theme__delete-button');
        deleteButtonDOM.addEventListener('click', () => {
             themeInputsGroup.remove();
        });
        subjectFormDOM.insertBefore(themeInputsGroup, buttonsGroup);
    });


});