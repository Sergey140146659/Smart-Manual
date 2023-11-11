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


//  Global Vars

    let currentToggles = {
        "faq": false,
        "article": true,
        "law": false
    };

    let currentTarget = '';

    function changeCurrentTarget (value) {
        currentTarget = value;
        const articleNameField = document.querySelectorAll('.rate_form_article_name');
        articleNameField.forEach(item => {
            item.textContent = currentTarget;
        });
    }


//  Toggle to modify answer

    function disableAllToggles (toggleButtons) {
        currentToggles = {
            "faq": false,
            "article": false,
            "law": false
        }

        toggleButtons.forEach(button => {
             button.classList.remove('active');
             button.classList.add('disabled');
        });
    }

    const toggleButtons = document.querySelectorAll('.mod_tag_button');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            disableAllToggles(toggleButtons);

            let type = button.dataset.type;

            currentToggles[type] = true;
            button.classList.remove('disabled');
            button.classList.add('active');

            showArticles();
            currentTarget = '';
        });
    });


//  Choose Article

    async function showArticles() {
        let articlesListDOM = document.querySelector('.articles_list');
        articlesListDOM.innerHTML = '';

        if (currentToggles["faq"]) {
            let faq = await getRequest('/article/get_faq_list');
            buildArticlesDOM(faq, articlesListDOM);
            console.log(faq);
        } else if (currentToggles["article"]) {
            let articles = await getRequest('/article/get_articles_list');
            buildArticlesDOM(articles, articlesListDOM);
            console.log(articles);
        }

        function buildArticlesDOM (tree, articlesListDOM) {
            let prevEl = articlesListDOM ;
            for (let i = 0; i < tree.length; i++) {
                if (Array.isArray(tree[i])) {
                    let buttonArrow = document.createElement('div');
                    buttonArrow.classList.add('article_acc_button');
                    buttonArrow.innerHTML = `
                        <img class="acc_button_arrow" src="../static/images/down-arrow-icon.svg" alt="Стрелка вниз">
                    `
                    let articleChooseButton = prevEl.querySelector('.article_item_button');
                    articleChooseButton.append(buttonArrow);

                    let newList = document.createElement('ul');
                    newList.classList.add('d-none', 'article_embedded_ul');
                    prevEl.append(newList);
                    buildArticlesDOM(tree[i], newList);


                    articleChooseButton.addEventListener('click', () => {
                        if (!event.target.classList.contains('target')) {
                            newList.classList.toggle('d-none');
                        }
                    });
                } else {
                    let item = document.createElement('li');
                    item.classList.add('article_item');
                    item.innerHTML = `
                        <button class="article_item_button">
                            <div class="article_item_choose_button">${tree[i]['name']}</div>
                        </button>
                    `
                    prevEl = item;
                    articlesListDOM.append(item);

                    let curButton = item.querySelector(".article_item_choose_button");
                    if (!tree[i]['is_parent']) {
                        curButton.classList.add('target');
                        curButton.addEventListener('click', () => {
                            const itemsList = document.querySelectorAll('.article_item');
                            itemsList.forEach(i => {
                                i.classList.remove('active');
                            });
                            item.classList.add('active');
                            changeCurrentTarget(tree[i]['name']);
                        });
                    }
                }
            }
        }
    }

    showArticles();

    function chooseArticle() {

    }


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


//  Message Rate Block

    function messageRateBlock (req, req_id) {

        const rateBlock = document.createElement('form');
        rateBlock.classList.add("rate_block_form");

        rateBlock.innerHTML = `
            <button type="button" class="rate_block_edit_button">Редактировать</button>
            <p class="rate_form_article_name d-none">Выберите статью...</p>
            <button type="submit" class="rate_form_submit d-none">Отправить</button>
        `;

        const editButton = rateBlock.querySelector('.rate_block_edit_button');
        const articleName = rateBlock.querySelector('.rate_form_article_name');
        const articleEditSubmit = rateBlock.querySelector('.rate_form_submit');

        editButton.addEventListener('click', () => {

            articleEditSubmit.classList.toggle('d-none');
            articleName.classList.toggle('d-none');

            if (currentTarget == '') {
                articleName.textContent = 'Выберите статью...';
            } else {
                articleName.textContent = currentTarget;
            }
        });

        articleEditSubmit.addEventListener('click', (event) => {
            event.preventDefault();
            let res = postRequest('/article/add_question', JSON.stringify({
                'query': req,
                'article_name': articleName.textContent
            }))
            .then(data => {
               if (data.status == 'success') {
                   rateBlock.innerHTML = `<span class="success_message">Успешно</span>`;
                   changeCurrentTarget('');
                   postRequest(`/query/query_set_fixed?query_id=${req_id}`);
               } else {
                   rateBlock.innerHTML = `<span class="error_message">Ошибка</span>`;
               };
            });
        });

        return rateBlock;
    }


    const botMessageContent = function (message, res, req) {

        message.innerHTML = '';
        let data = res["data"];

        if (data["is_valid"] == 0)  {
            message.innerHTML = `
            <p>${data["comment"]}<p>
            `
        } else if (data["is_valid"] == 1) {
            let isFirst = true;

            message.append(messageRateBlock(req, res.id));

            const ans = data["ans"];

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
                            <p>Подробнее можете ознакомиться:</p>
                            <a class="article-link" href=${faq.main_faq.faq_link} target="_blank">${faq.main_faq.faq_name}</a>
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
                            <p>Подробнее можете ознакомиться:</p>
                            <a class="article-link" href=${article.main_article.article_link} target="_blank">${article.main_article.article_name}</a>
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

                    message.append(accBlock);
                }
            }
        }
    }


//  Send form

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

        postRequest('/article/get_answer_without_classification', JSON.stringify(sendData))
            .then(data => {
                botMessageContent(answerMessage, data, req)
                messagesBlock.scrollTo(0, messagesBlock.scrollHeight);
            });
    }


//  Form Sendlers

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
