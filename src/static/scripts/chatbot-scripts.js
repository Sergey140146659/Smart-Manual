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
        makeInputMessageAvailable();
    }

    function makeInputMessageAvailable () {
        const inputMessage = document.querySelector('.request_input');
        inputMessage.removeAttribute("disabled");
        inputMessage.setAttribute("placeholder", "Спросите что-нибудь...")
    }

    function clearSubjectsActiveButton () {
        const activeButton = document.querySelector('.subject-list__item__button.active');
        if (activeButton) {
            activeButton.classList.remove('active');
        }
    }


//  Send Message

    const messageFormDOM = document.querySelector('.messanger_form');
    const messageInputDOM = document.querySelector('.request_input');
    messageInputDOM.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            messageFormDOM.dispatchEvent(new Event('submit'));
        }
    });
    messageFormDOM.addEventListener('submit', async (e) => {
        e.preventDefault();
        const messageInput = messageFormDOM.querySelector('.request_input');
        const message = messageInput.value;
        createUserMessage(message);

        const url = `../answer/get_answer?subject_name=${subjectTargetName}&request=${message}`
        await createBotMessage(getRequest(url));
        messageInput.value = '';
    });


//  Crete Message

    function createUserMessage (message) {
        const messageBlockDOM = document.querySelector('.prev_messages_block');
        const messageDOM = document.createElement('div');
        messageDOM.classList.add('user_message');
        messageDOM.textContent = message;
        messageBlockDOM.append(messageDOM);
    }

    async function createBotMessage (promise) {
        const messageBlockDOM = document.querySelector('.prev_messages_block');
        const messageDOM = document.createElement('div');
        messageDOM.classList.add('request_message');
        messageDOM.innerHTML = `
            <div class="loader-container">
                <span class="loader"></span>
            </div>
        `;
        messageBlockDOM.append(messageDOM);
        messageBlockDOM.scrollTo(0, messageBlockDOM.scrollHeight);

        const message = await promise;
        if (message.status == 'OK') {
            messageDOM.innerHTML = `
                <p>${message.text}</p>
            `
            const themeList = document.createElement('ul');

            for (theme of message.data) {
                themeList.innerHTML += `
                    <li>
                        <a class="pdf-link" href="../ml/preprocessing_data/${theme.pdf_name}#page=${theme.page_start}" target="_blank">${theme.theme_name}</a>
                        <span class="pdf-pages">стр.${theme.page_start-theme.page_end ? `${theme.page_start}-${theme.page_end}` : theme.page_start}</span>
                    </li>
                `;
            }
            messageDOM.append(themeList);
            messageBlockDOM.scrollTo(0, messageBlockDOM.scrollHeight);
        }
    }
});