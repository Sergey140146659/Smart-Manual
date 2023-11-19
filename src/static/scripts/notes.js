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
    let themeTargetName = '';


//   Get Wide Subject List

    async function getWideSubjectList () {
        const wideSubjectsList = await getRequest('../db/wide_subject_list');
        clearWideSubjectListDOM();
        buildWideSubjectListDOM(wideSubjectsList);
    }
    getWideSubjectList();

    function buildWideSubjectListDOM (subjectList) {
        for (subject of subjectList) {
            createWideSubjectDOM(subject);
        }
    }

    function clearWideSubjectListDOM () {
        const wideSubjectsListDOM = document.querySelector('.wide-subject-list');
        wideSubjectsListDOM.innerHTML = '';
    }

    function createWideSubjectDOM (subject) {
        const wideSubjectsListDOM = document.querySelector('.wide-subject-list');

        const newSubject = document.createElement('li');
        newSubject.classList.add('wide-subject-list__item');
        newSubject.innerHTML = `
            <span>${subject.name}</span>
        `;
        let filesList = [];
        for (theme of subject.themes) {
            if (filesList.indexOf(theme.file_name) == -1) {
                filesList.push(theme.file_name);
            }
        }
        for (file of filesList) {
            newSubject.innerHTML += `
                <p><a href="../ml/preprocessing_data/${file}" class="wide-subject-list__subject-file" target="_blank">${file}</a></p>
            `;
            const themesListDOM = document.createElement('ul');
            themesListDOM.classList.add('wide-subject-list__themes-list');
            for (theme of subject.themes) {
                if (theme.file_name == file) {
                    themesListDOM.innerHTML += `
                        <li class="wide-subject-list__theme-item">
                            <button type="button" class="wide-subject-list__theme-item__button" data-subject="${subject.name}">${theme.name}</button>
                        </li>
                    `;
                }
            }
            newSubject.append(themesListDOM);
        }

        wideSubjectsListDOM.append(newSubject);

        const themesButtonsListDOM = newSubject.querySelectorAll('.wide-subject-list__theme-item__button');
        for (themeButtonDOM of themesButtonsListDOM) {
            const curThemeButtonDOM = themeButtonDOM;
            themeButtonDOM.addEventListener('click', () => chooseTheme(curThemeButtonDOM));
        }

        return newSubject;
    }


//  Choose Theme

    function chooseTheme (themeButtonDOM) {
        clearThemeActiveButton();
        themeButtonDOM.classList.add('active');
        themeTargetName = themeButtonDOM.textContent;
        subjectTargetName = themeButtonDOM.dataset.subject;
        uploadAvailable();
        showNote(subjectTargetName, themeTargetName);
    }

    function uploadAvailable () {
        const uploadButton = document.querySelector('.notes-writing__form__send-button');
        const noteTextarea = document.querySelector('.notes-writing__form__textarea');
        uploadButton.removeAttribute("disabled");
        noteTextarea.removeAttribute("disabled");
        noteTextarea.setAttribute("placeholder", "Напишите что-нибудь...");
    }


    function clearThemeActiveButton () {
        const activeButton = document.querySelector('.wide-subject-list__theme-item__button.active');
        if (activeButton) {
            activeButton.classList.remove('active');
        }
    }


//  Send note
    
    const noteFormDOM = document.querySelector('.notes-writing__form');
    noteFormDOM.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formTextarea = noteFormDOM.querySelector('.notes-writing__form__textarea');
        const note = formTextarea.value;
        const url = `../db/write_theme_notes?subject_name=${subjectTargetName}&theme_name=${themeTargetName}&note=${note}`;
        response = await postRequest(url);
        console.log(response);
        
        const buttonsGroupDOM = document.querySelector('.buttons-group');
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


//  Show note

    async function showNote (subjectName, themeName) {
        const formTextarea = document.querySelector('.notes-writing__form__textarea');
        const url = `../db/theme_notes?subject_name=${subjectName}&theme_name=${themeName}`;
        const notes = await getRequest(url);
        formTextarea.value = notes;
    }
});