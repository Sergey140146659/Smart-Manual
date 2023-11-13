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


    let subjectTargetName = '';


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
    }

    function clearSubjectsActiveButton () {
        const activeButton = document.querySelector('.loaded-db__item__button.active');
        if (activeButton) {
            activeButton.classList.remove('active');
        }
    }

});