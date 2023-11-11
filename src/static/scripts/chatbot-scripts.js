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


//    Check Token

    const authSection = document.querySelector(".auth_section");

    function checkToken() {
        const systemToken = getCookie().system_token;
        const sendJson = JSON.stringify({"system_token": systemToken});

        if (systemToken) {
            postRequest('/system/auth_system', sendJson)
                .then(data => {
                    if (data.status == "success") {
                        authSection.classList.add('d-none');
                        console.log("success")
                    } else {
                        console.log("err")
                    }
                });
        } else {
            authSection.classList.remove('d-none');
        }
    }

    checkToken();


//    Auth System Token

    const authSystemForm = document.querySelector('.chatbot_auth_modal_window_form');

    authSystemForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(authSystemForm);
        const systemToken = formData.get('chatbot_auth_token');

        const sendJson = JSON.stringify({'system_token': systemToken});

        postRequest('/system/auth_system', sendJson)
            .then(data => {
                if (data.status == "success") {
                    checkToken();
                } else {
                    console.log("err: Can`t write token")
                }
            });
    });


//    Chats List DOM

    const chatsButtons = document.querySelectorAll('.chats_list_item_button');
    let activeChatButton = document.querySelector('.chats_list_item_button.active');

    chatsButtons.forEach(button => {
        button.addEventListener('click', () => {
            activeChatButton.classList.remove('active');
            button.classList.add('active');

            activeChatButton = button;
        });
    });


//    Toggle to modify answer

    let currentToggles = {
        "faq": true,
        "article": true,
        "law": true
    };

    const toggleButtons = document.querySelectorAll('.mod_tag_button');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            let type = button.dataset.type;
            if (currentToggles[type] === false) {
                currentToggles[type] = true;
                button.classList.remove('disabled');
                button.classList.add('active');
            } else {
                currentToggles[type] = false;
                button.classList.remove('active');
                button.classList.add('disabled');
            }
        });
    });


//  Request send

    const requestForm = document.getElementById('request-form');
    const messagesBlock = document.querySelector('.prev_messages_block');

    const botMessageDOM = function () {
        const message = document.createElement('div');
        message.classList.add('request_message');
        message.innerHTML = `
            <div class="loader-container">
                <span class="loader"></span>
            </div>
        `;
        messagesBlock.append(message);

        return message;
    }


    const userMessageDOM = function (msg) {
        const message = document.createElement('div');
        message.classList.add('user_message');
        message.innerHTML = msg;
        messagesBlock.append(message);
    }


    const botMessageContent = function (message, res, req) {

        message.innerHTML = '';
        let data = res["data"];
        console.log(res);

        if (data["is_valid"] == 0)  {
            message.innerHTML = `
                <p>${data["comment"]}<p>
                <button class="search_without_classification_button">Все равно искать</button>
            `
            const button = message.querySelector('.search_without_classification_button');
            button.addEventListener('click', () => {
                let sendData = {
                    "chat_id": 1,
                    "query": req,
                    "questions": currentToggles
                }
                postRequest('/article/get_answer_without_classification', JSON.stringify(sendData))
                .then(data => {
                    botMessageContent(message, data, req)
                });
            });

        } else if (data["is_valid"] == 1) {
            const ans = data["ans"];
            let isFirst = true;

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
                        <div class="acc_content ${isFirst ? '' : 'd-none'}">
                            <p>${faq.text_paragraphs}</p>
                            <p>Подробнее можете ознакомиться:
                                 <a class="article-link" href=${faq.main_faq.faq_link} target="_blank">${faq.main_faq.faq_name}</a>
                            </p>
                            <p class="also_crawling">Также может быть полезно:</p>
                            <ul class="faq_list"></ul>
                        </div>
                    `
                    isFirst = false;

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

                    isUseful(accContent, key, res['id']);

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
                        <div class="acc_content ${isFirst ? '' : 'd-none'}">
                            <p>${article.text_paragraphs}</p>
                            <p>Подробнее можете ознакомиться:
                                 <a class="article-link" href=${article.main_article.article_link} target="_blank">${article.main_article.article_name}</a>
                            </p>
                            <p class="also_crawling">Также может быть полезно:</p>
                            <ul class="article_list"></ul>
                        </div>
                    `
                    isFirst = false;

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

                    isUseful(accContent, key, res['id']);

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
                        <div class="acc_content ${isFirst ? '' : 'd-none'}">
                            <ul class="law_list"></ul>
                        </div>
                    `
                    isFirst = false;

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

                    isUseful(accContent, key, res['id']);

                    message.append(accBlock);
                }
            }
        }
    }


//  Is Useful

    function isUseful (blockDOM, blockName, queryId) {
        const usefulBlock = document.createElement('div');
        usefulBlock.classList.add('useful_block');
        usefulBlock.innerHTML = `
            <button class="answer_like">
                <img class="like_image" src="../static/images/like-icon.svg" alt="Лайк">
            </button>
            <button class="answer_dislike">
                <img class="like_image" src="../static/images/dislike-icon.svg" alt="Дизлайк">
            </button>
        `

        const like = usefulBlock.querySelector('button.answer_like');
        like.addEventListener('click', () => {
            postRequest('/article/is_useful', JSON.stringify({
                'query_id': queryId,
                'answer_type': blockName,
                'useful_rate': true
            }));
            like.classList.add('active');
            dislike.classList.remove('active');
        });

        const dislike = usefulBlock.querySelector('button.answer_dislike');
        dislike.addEventListener('click', () => {
            postRequest('/article/is_useful', JSON.stringify({
                'query_id': queryId,
                'answer_type': blockName,
                'useful_rate': false
            }));
            dislike.classList.add('active');
            like.classList.remove('active');
        });

        blockDOM.append(usefulBlock);
    }


//    Send form

    let reqInput = document.querySelector('.request_input');

    function sendForm () {
        const requestFormData = new FormData(requestForm);
        let req = requestFormData.get('request');

        let sendData = {
            "chat_id": 1,
            "query": req,
            "questions": currentToggles
        }

        reqInput.value = '';

        userMessageDOM(req);
        let answerMessage = botMessageDOM();
        messagesBlock.scrollTo(0, messagesBlock.scrollHeight);

        postRequest('/article/get_answer', JSON.stringify(sendData))
            .then(data => {
                console.log(data);
                botMessageContent(answerMessage, data, req)
                messagesBlock.scrollTo(0, messagesBlock.scrollHeight);
            });
    }


//    Form Sendlers

    requestForm.addEventListener('submit', (event) => {
        event.preventDefault();

        sendForm();
    });

    reqInput.addEventListener('keypress', function(event) {
        if (event.keyCode == 13 && !event.shiftKey) {
            event.preventDefault();
            sendForm();
        }
    });
});