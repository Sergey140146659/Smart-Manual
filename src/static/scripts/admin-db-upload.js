window.addEventListener('DOMContentLoaded', () => {

//  Post Request

    async function postRequest(url, formData) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(error);
        }
    }


//  Get Request

    const getRequest = async (url) => {
        const response = await fetch(url, {
            method: 'GET'
        });
        return response.json();
    }


    let subjectTargetName = '';


// Subject Add Form

    const subjectAddFormDOM = document.querySelector(".add-subject-form");
    subjectAddFormDOM.addEventListener('submit', (e) => {
        e.preventDefault();
        const subjectNameInput = document.querySelector('.subject-form__input');
        const newSubjectName = subjectNameInput.value;

        const subjectItemDOM = createSubjectDOM(newSubjectName);
        chooseSubject(subjectItemDOM.querySelector('button'));
        subjectNameInput.value = '';
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
        const subjectListDOM = document.querySelector('.subject-list');
        subjectListDOM.innerHTML = '';
    }

    function createSubjectDOM (subjectName) {
        const subjectsListDOM = document.querySelector('.subject-list');

        const newSubject = document.createElement('li');
        newSubject.classList.add('subject-list__item');
        newSubject.innerHTML = `
            <button type="button" class="subject-list__item__button">${subjectName}</button>
        `;
        const newSubjectButton = newSubject.querySelector('.subject-list__item__button');
        newSubjectButton.addEventListener('click', () => chooseSubject(newSubjectButton));
        subjectsListDOM.append(newSubject);
        return newSubject;
    }


//  Choose Subject

    function chooseSubject (subjectButtonDOM) {
        clearSubjectsActiveButton();
        subjectButtonDOM.classList.add('active');
        subjectTargetName = subjectButtonDOM.textContent;
        uploadAvailable();
    }

    function uploadAvailable () {
        const uploadButton = document.querySelector('.send-button');
        uploadButton.removeAttribute("disabled");
    }

    function clearSubjectsActiveButton () {
        const activeButton = document.querySelector('.subject-list__item__button.active');
        if (activeButton) {
            activeButton.classList.remove('active');
        }
    }


//  Send Subject Form

    const subjectFormDOM = document.querySelector('.subject-form');
    subjectFormDOM.addEventListener('submit', async (e) => {
        e.preventDefault();
        const curThemesNameArr = Array.from(subjectFormDOM.querySelectorAll('.theme-name__input')).map(input => input.value);
        const curThemesStartPageArr = Array.from(subjectFormDOM.querySelectorAll('.page-num__input#start-page-num')).map(input => input.value);
        const curThemesEndPageArr = Array.from(subjectFormDOM.querySelectorAll('.page-num__input#end-page-num')).map(input => input.value);
        let themesArr = [];
        for (let i = 0; i < curThemesNameArr.length; i++) {
            themesArr.push({'theme_name': curThemesNameArr[i],
                            'page_start': curThemesStartPageArr[i],
                            'page_end': curThemesEndPageArr[i]});
        }
        const themesJSON = JSON.stringify(themesArr);
        const fileInput = document.querySelector('.upload-file-form__input');
        const file = fileInput.files[0];

        const formData = new FormData();
        formData.append("subject_file", file);
        formData.append("subject_name", subjectTargetName);
        formData.append("themes", themesJSON);

        const response = await postRequest('../db/subject_db_upload', formData);

        const buttonsGroupDOM = document.querySelector('.subject__buttons-group');
        if (response.status != "ok") {
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('error_message');
            errorMessage.textContent = 'Ошибка';
            buttonsGroupDOM.append(errorMessage);

            setTimeout(() => {
                errorMessage.remove();
            }, 2000);
        } else {
            const successMessage = document.createElement('div');
            successMessage.classList.add('success_message');
            successMessage.textContent = 'Успех';
            buttonsGroupDOM.append(successMessage);

            setTimeout(() => {
                successMessage.remove();
            }, 2000);
        }
    });


//  Add Theme DOM

    const addThemeButton = document.querySelector('.subject__add-theme-button');
    addThemeButton.addEventListener('click', () => {
        const subjectFormDOM = document.querySelector('.subject-form');
        const buttonsGroup = document.querySelector('.subject__buttons-group');
        const themeInputsGroup = document.createElement('div');
        themeInputsGroup.classList.add('theme-inputs-group');
        themeInputsGroup.innerHTML = `
            <label class="d-none" for="theme">Название темы</label>
            <input class="subject-form__input theme-name__input" type="text" id="theme" name="theme" placeholder="Название темы" autocomplete="off">
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