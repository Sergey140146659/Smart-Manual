window.addEventListener('DOMContentLoaded', () => {

//  Get Request

    const getRequest = async (url) => {
        const response = await fetch(url, {
            method: 'GET'
        });
        return response.json();
    }


//  Files List

    async function getFilesList () {
        const response = await getRequest('../db/files_list');
        for (subject in response) {
            createSubjectCard(subject, response[subject]);
        }
    }
    getFilesList();


    function createSubjectCard (subjectName, filesList) {
        const filesDOM = document.querySelector('.files');
        const subjectCard = document.createElement('div');
        subjectCard.classList.add('subject-card');
        subjectCard.innerHTML = `
            <span class="subject-card__subject-name">${subjectName}</span>
            <ul class="files-list"></ul>
        `;
        const filesListDOM = subjectCard.querySelector('.files-list');
        for (file of filesList) {
            filesListDOM.innerHTML += `
                <li class="files-item">
                    <a class="files-link" href="../ml/preprocessing_data/${file}" target="_blank">${file}</a>
                </li>
            `;
        }
        filesDOM.append(subjectCard);
    }
});