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
        console.log(subjectList)
        for (subject of subjectList) {
            console.log(subject);
            createWideSubjectDOM(subject);
        }
    }

    function clearWideSubjectListDOM () {
        const wideSubjectsListDOM = document.querySelector('.wide-subject-list');
        wideSubjectsListDOM.innerHTML = '';
    }

    function clearWideSubjectListDOM (subject) {
        const wideSubjectsListDOM = document.querySelector('.wide-subject-list');

        const newSubject = document.createElement('li');
        newSubject.classList.add('subject-list__item');
        newSubject.innerHTML = `
            ${subject["name"]}
        `;
        subjectsListDOM.append(newSubject);
        return newSubject;
    }

});