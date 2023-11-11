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
        "faq": true,
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


//  Choose Article

    async function showArticles() {
        let articlesListDOM = document.querySelector('.articles_list');
        articlesListDOM.innerHTML = '';

        if (currentToggles["article"]) {
            let articles = await getRequest('/article/get_articles_list');
            buildArticlesDOM(articles, articlesListDOM);
        }
        if (currentToggles["faq"]) {
            let faq = await getRequest('/article/get_faq_list');
            buildArticlesDOM(faq, articlesListDOM);
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


    const messagesBlock = document.querySelector('.prev-messages-block');

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

        if (res["is_valid"] == 0)  {
            message.innerHTML = `
            <p>${res["comment"]}<p>
            `
        } else if (res["is_valid"] == 1) {
            let isFirst = true;

            message.append(messageRateBlock(req, res.id));

            const ans = JSON.parse(res["result"]);

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

                    if (res.useful_faq != null) {
                        const usefulBlock = document.createElement('div');
                        usefulBlock.classList.add('useful_block');

                        if (res.useful_faq === true) {
                            usefulBlock.innerHTML = `
                                <button class="answer_like active">
                                    <img class="like_image" src="../static/images/like-icon.svg" alt="Лайк">
                                </button>
                            `;
                        };

                        if (res.useful_faq === false) {
                            usefulBlock.innerHTML = `
                                <button class="answer_dislike active">
                                    <img class="like_image" src="../static/images/dislike-icon.svg" alt="Дизлайк">
                                </button>
                            `;
                        };

                            accBlock.append(usefulBlock);
                    };

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

                    const usefulBlock = document.createElement('div');
                    usefulBlock.classList.add('useful_block');

                    if (res.useful_article === true) {
                        usefulBlock.innerHTML = `
                            <button class="answer_like active">
                                <img class="like_image" src="../static/images/like-icon.svg" alt="Лайк">
                            </button>
                        `;
                    };

                    if (res.useful_article === false) {
                        usefulBlock.innerHTML = `
                            <button class="answer_dislike active">
                                <img class="like_image" src="../static/images/dislike-icon.svg" alt="Дизлайк">
                            </button>
                        `;
                    };

                    accBlock.append(usefulBlock);

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

                     const usefulBlock = document.createElement('div');
                    usefulBlock.classList.add('useful_block');

                    if (res.useful_law === true) {
                        usefulBlock.innerHTML = `
                            <button class="answer_like active">
                                <img class="like_image" src="../static/images/like-icon.svg" alt="Лайк">
                            </button>
                        `;
                    };

                    if (res.useful_law === false) {
                        usefulBlock.innerHTML = `
                            <button class="answer_dislike active">
                                <img class="like_image" src="../static/images/dislike-icon.svg" alt="Дизлайк">
                            </button>
                        `;
                    };

                    accBlock.append(usefulBlock);

                    message.append(accBlock);
                }
            }
        }
    }


//  Show Query History

    const pageSize = 10;
    let currentPage = 1;
    let currentFilters = {"not_fixed": true};
    const urlParams = new URLSearchParams(window.location.search);
    const chatId = urlParams.get('chat_id');
    const systemId = urlParams.get('system_id');
    const dateStart = urlParams.get('date_start');
    const dateEnd = urlParams.get('date_end');

    const filtersForm = document.querySelector('.filter_form');

    if (chatId) {
         currentFilters.chat_id = chatId;
         const DOMChatId = filtersForm.querySelector('#chat_id');
         DOMChatId.value = chatId;
    }
    if (systemId) {
        currentFilters.system_id = systemId;
        const DOMSystemId = filtersForm.querySelector('#system_id');
        DOMSystemId.value = systemId;
    }
    if (dateStart) {
        currentFilters.date_start = dateStart;
        const DOMDateStart = filtersForm.querySelector('#date_start');
        DOMDateStart.value = dateStart;
    }
    if (dateEnd) {
        currentFilters.date_end = dateEnd;
        const DOMDateEnd = filtersForm.querySelector('#date_end');
        DOMDateEnd.value = dateEnd;
    }
    postRequest(`/query/get_filtered_queries?page_size=${pageSize}&current_page=${currentPage}`, JSON.stringify(currentFilters))
    .then(data => {
        showQueries(data);
    });


    function showQueries (queriesList) {
        const messagesContainer = document.querySelector('.prev-messages-block');

        queriesList.forEach(item => {
            userMessageDOM(item.query);
            botMessageContent(botMessageDOM(), item, item.query)
        });
    };


    filtersForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const requestFormData = new FormData(filtersForm);

        const params = new URLSearchParams();
        for (const [key, value] of requestFormData.entries()) {
          if (value !== "") {
            params.append(key, value);
          }
        }

        currentFilters = Object.fromEntries(params);

        const notFixed = filtersForm.querySelector('#not_fixed');
        if (notFixed.checked) {
            currentFilters.not_fixed = false;
        }

        const random = filtersForm.querySelector('#random');
        if (random.checked) {
            currentFilters.random = true;
        }

        const usefulFaq = filtersForm.querySelector('#useful_faq');
        if (usefulFaq.checked) {
            currentFilters.useful_faq = false;
        }

        const usefulArticle = filtersForm.querySelector('#useful_article');
        if (usefulArticle.checked) {
            currentFilters.useful_article = false;
        }

        const usefulLaw = filtersForm.querySelector('#useful_law');
        if (usefulLaw.checked) {
            currentFilters.useful_law = false;
        }

        currentPage = 1;
        postRequest(`/query/get_filtered_queries?page_size=${pageSize}&current_page=${currentPage}`, JSON.stringify(currentFilters))
        .then(data => {
            messagesBlock.innerHTML = '';
            showQueries(data);
        });
    });

    messagesBlock.addEventListener('scroll', async () => {
        let scrollHeight = messagesBlock.scrollHeight;
        let currentScroll = messagesBlock.scrollTop;
        if (scrollHeight - 912 <= currentScroll) {
            currentPage++;
            messagesList = await postRequest(`/query/get_filtered_queries?page_size=${pageSize}&current_page=${currentPage}`, JSON.stringify(currentFilters));
            showQueries(messagesList);
        }
    });
});