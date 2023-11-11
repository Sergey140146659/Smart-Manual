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


//  Messages DOM

    const botMessageDOM = function (messagesParentDOM) {
        const message = document.createElement('div');
        message.classList.add('request_message');
        message.innerHTML = `
            <div class="loader-container">
                <span class="loader"></span>
            </div>
        `;
        messagesParentDOM.append(message);

        return message;
    }

    const userMessageDOM = function (msg, messagesParentDOM) {
        const message = document.createElement('div');
        message.classList.add('user_message');
        message.innerHTML = msg;
        messagesParentDOM.append(message);
    }


//  Answer Message Content

    const botMessageContent = function (message, res) {

        message.innerHTML = '';

        if (res["is_valid"] == 0)  {
            message.innerHTML = `
            <p>Ничего не найдено<p>
            `
        } else if (res["is_valid"] == 1) {
            const ans = res["data"];

            for (let key in ans) {

                //  FAQ Block

                if (key === "faq" && ans[key]) {

                    const faq = ans["faq"];
                    const accBlock = document.createElement('div');
                    accBlock.classList.add('chatbot_message_block')

                    accBlock.innerHTML = `
                        <button class="acc_button">
                            <span>FAQ</span>
                            <img class="acc_button_arrow" src="../static/images/down-arrow-icon.svg" alt="Стрелка вниз">
                        </button>
                        <div class="acc_content">
                            <p>${faq.text_paragraphs}</p>
                            <p>Подробнее можете ознакомиться:
                                 <a class="article-link" href=${faq.main_faq.faq_link} target="_blank">${faq.main_faq.faq_name}</a>
                            </p>
                            <p class="also_crawling">Также может быть полезно:</p>
                            <ul class="faq_list"></ul>
                        </div>
                    `

                    //  Also be crawling list

                    const faqList = accBlock.querySelector('.faq_list');

                    faq["faqs"].forEach(item => {
                        const faq_item = document.createElement('li');
                        faq_item.classList.add('article-user-item');
                        faq_item.innerHTML = `
                            <a class="article-link" href=${item["faq_link"]} target="_blank">${item["faq_name"]}</a>
                        `

                        faqList.append(faq_item);
                    });

                    //  Acc Button

                    const accButton = accBlock.querySelector('.acc_button');
                    const accContent = accBlock.querySelector('.acc_content');

                    accButton.addEventListener('click', () => {
                        accContent.classList.toggle('d-none');
                    });

                    message.append(accBlock);
                }


                //  Article Block

                if (key === "article" && ans[key]) {

                    const article = ans["article"];
                    const accBlock = document.createElement('div');
                    accBlock.classList.add('chatbot_message_block')

                    accBlock.innerHTML = `
                        <button class="acc_button">
                            <span>Инструкция</span>
                            <img class="acc_button_arrow" src="../static/images/down-arrow-icon.svg" alt="Стрелка вниз">
                        </button>
                        <div class="acc_content d-none">
                            <p>${article.text_paragraphs}</p>
                            <p>Подробнее можете ознакомиться:
                                 <a class="article-link" href=${article.main_article.article_link} target="_blank">${article.main_article.article_name}</a>
                            </p>
                            <p class="also_crawling">Также может быть полезно:</p>
                            <ul class="article_list"></ul>
                        </div>
                    `

                    //  Also be crawling list

                    const articleList = accBlock.querySelector('.article_list');

                    article["articles"].forEach(item => {
                        const article_item = document.createElement('li');
                        article_item.classList.add('article-user-item');
                        article_item.innerHTML = `
                            <a class="article-link" href=${item["article_link"]} target="_blank">${item["article_name"]}</a>
                        `

                        articleList.append(article_item);
                    });

                    //  Acc Button

                    const accButton = accBlock.querySelector('.acc_button');
                    const accContent = accBlock.querySelector('.acc_content');

                    accButton.addEventListener('click', () => {
                        accContent.classList.toggle('d-none');
                    });

                    message.append(accBlock);
                }


                //  Law Block

                if (key === "law" && ans[key]) {

                    const law = ans["law"];
                    const accBlock = document.createElement('div');
                    accBlock.classList.add('chatbot_message_block')

                    accBlock.innerHTML = `
                        <button class="acc_button">
                            <span>Законы</span>
                            <img class="acc_button_arrow" src="../static/images/down-arrow-icon.svg" alt="Стрелка вниз">
                        </button>
                        <div class="acc_content d-none">
                            <ul class="law_list"></ul>
                        </div>
                    `

                    //  Also be crawling list

                    const lawList = accBlock.querySelector('.law_list');

                    law["laws"].forEach(item => {
                        const law_item = document.createElement('li');
                        law_item.classList.add('article-user-item');
                        law_item.innerHTML = `
                            <a class="article-link" href=${item["law_link"]} target="_blank">${item["law_name"]}</a>
                        `

                        lawList.append(law_item);
                    });

                    //  Acc Button

                    const accButton = accBlock.querySelector('.acc_button');
                    const accContent = accBlock.querySelector('.acc_content');

                    accButton.addEventListener('click', () => {
                        accContent.classList.toggle('d-none');
                    });

                    message.append(accBlock);
                }
            }

        }
    }


//  Load Chat Table

    function showChats (chatsList) {
        const table = document.querySelector(".chats-list-body");

        chatsList.forEach(item => {
            let newTr = document.createElement("tr");
            newTr.classList.add("systems-list__item");
            newTr.innerHTML = `
                <th class="chat_id">${item.id}</th>
                <th class="chat_system_id">${item.systemId}</th>
                <th class="chat_user_id">${item.userId}</th>
                <th class="chat_is_anon">${item.isAnonymous}</th>
                <th class="chat_session_id">${item.sessionId}</th>
                <th class="chat_name">${item.name}</th>
                <th class="chat_history">
                    <a class="chat_history_link" href="/pages/admin_queries?chat_id=${item.id}" target="_blank">Сообщения</a>
                </th>
            `
            table.append(newTr);


            //  Chat Messages History

            let chatHistoryButton = newTr.querySelector('.chat_history_button');

//            chatHistoryButton.addEventListener('click', () => {
//                showChatMessages(item.id);
//            });

        });
    }

    const loadChatTable = async function () {
        let response = await getRequest("/chat/get_all_chats");
        let chatsList = response["data"];

        showChats(chatsList);
    }

    loadChatTable();


//  Clear Chat Table

    const chatTable = document.querySelector('.chats-list-body');

    function clearChatTable () {
        chatTable.innerHTML = ``;
    }


//  Get Messages History


//  Show Messages History

    let showMessagesHistory = function (messagesParentDOM, messagesList) {
        messagesList["query_list"].forEach(item => {
            userMessageDOM(item.query, messagesParentDOM);
            let botMessage = botMessageDOM(messagesParentDOM);

            botMessageContent(botMessage, {"data": JSON.parse(item.result), "is_valid": item.is_valid});

        });
    }

//  Show chat messages

    const showChatMessages = async function (chatId) {
        const modal = document.querySelector('.modal');
        const closeModalElements = document.querySelectorAll('.close-modal-area');

        modal.classList.remove('hidden');

        closeModalElements.forEach(item => {
            item.addEventListener('click', (e) => {
                if (e.target.classList.contains('close-modal-area')) {
                    modal.classList.add('hidden');
                }
            });
        });

        let pageNumber = 1;
        const pageSize = 10;

        const url = `/chat/get_chat_history/${chatId}?page_number=${pageNumber}&page_size=${pageSize}`;
        let messagesList = await getRequest(url);

        const messagesBlock = modal.querySelector('.modal_window_messages_block');

        messagesBlock.innerHTML = '';

        showMessagesHistory(messagesBlock, messagesList);

        messagesBlock.addEventListener('scroll', async () => {
            let scrollHeight = messagesBlock.scrollHeight;
            let currentScroll = messagesBlock.scrollTop;
            if (scrollHeight-524 == currentScroll) {
                pageNumber++;
                const url = `/chat/get_chat_history/${chatId}?page_number=${pageNumber}&page_size=${pageSize}`;
                messagesList = await getRequest(url);
                showMessagesHistory(messagesBlock, messagesList);
            }
        });
    }


//  Filter Chats

    function filterChats() {
        const filterForm = document.querySelector('.filter_form');

        filterForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(filterForm);

            let sendFilter = {};
            formData.forEach(function(value, key) {
                if (value != "") {
                    sendFilter[key] = value;
                }
            });

            postRequest('/chat/get_filtered_chats', JSON.stringify(sendFilter))
            .then(res => {
                clearChatTable();
                showChats(res["data"]);
            });
        });
    }

    filterChats();
});