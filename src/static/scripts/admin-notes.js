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
        console.log(subject);
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
                <p class="wide-subject-list__subject-file">${file}</p>
            `;
            const themesListDOM = document.createElement('ul');
            themesListDOM.classList.add('wide-subject-list__themes-list');
            for (theme of subject.themes) {
                if (theme.file_name == file) {
                    themesListDOM.innerHTML += `
                        <li class="wide-subject-list__theme-item">
                            <button type="button" class="wide-subject-list__theme-item__button">${theme.name}</button>
                        </li>
                    `;
                }
            }
            newSubject.append(themesListDOM);
        }

        wideSubjectsListDOM.append(newSubject);
        return newSubject;
    }

});