window.addEventListener('DOMContentLoaded', () => {

//  Post Request

    const postRequest = async (url, data) => {
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


//  Choose Article

    async function showArticles() {
        let articlesListDOM = document.querySelector('.articles_list');
        articlesListDOM.innerHTML = '';


        let faq = await getRequest('/article/get_faq_list');
        let articles = await getRequest('/article/get_articles_list');
        buildArticlesDOM(articles, articlesListDOM);
        buildArticlesDOM(faq, articlesListDOM);

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
                            showArticlesQuestions(tree[i]['name']);
                        });
                    }
                }
            }
        }
    }

    showArticles();


//  Show Article Questions

    function createQuestionInput (question = '') {
        const queryInput = document.createElement('div');
        queryInput.classList.add('question_input_container');
        queryInput.innerHTML = `
            <input class="article_question_input" type="text" value="${question}">
            <button class="delete_question_button" type="button">
                <img src="../static/images/close-icon.svg" class="close_image">
            </button>
        `;
        const deleteButton = queryInput.querySelector("button");
        deleteButton.addEventListener('click', () => {
            queryInput.innerHTML = '';
        });

        return queryInput;
    }

    async function showArticlesQuestions (articleName) {
        const articleRatesFormDOM = document.querySelector('.articles_rates_form');

        articleRatesFormDOM.innerHTML = '';

        const articlesRatesListDOM = document.createElement('div');
        articlesRatesListDOM.classList.add('articles_rates_list');
        articleRatesFormDOM.append(articlesRatesListDOM);

        const questionsArr = await getRequest(`/article/get_article_question_list?article_name=${articleName}`);
        questionsArr.forEach(question => {

            const queryInput = createQuestionInput(question);

            articlesRatesListDOM.append(queryInput);
        });

    //  Add New Input

        const addInputButton = document.createElement('button');
        addInputButton.classList.add('article_add_question_button');
        addInputButton.setAttribute('type', 'button');
        addInputButton.textContent = 'Добавить вопрос';

        addInputButton.addEventListener('click', () => {
            const newInput = createQuestionInput();
            articlesRatesListDOM.append(newInput);
        });

        articleRatesFormDOM.append(addInputButton);

    //  Submit Form

        const submitButton = document.createElement('button');
        submitButton.classList.add('article_questions_submit');
        submitButton.setAttribute('type', 'button');
        submitButton.textContent = 'Отправить';

        articleRatesFormDOM.append(submitButton);

        submitButton.addEventListener('click', () => {

            let sendArr = [];
            const allQuestionsInputs = document.querySelectorAll('.article_question_input');
            allQuestionsInputs.forEach(input => {
                sendArr.push(input.value);
            });

            postRequest('/article/write_questions', JSON.stringify({
                "article_name": articleName,
                "query_list": sendArr
            }))
            .then(data => {
                const message = document.createElement('span');
                if (data.status == 'success') {
                    message.classList.add('message_success');
                    message.innerHTML = `
                        Успех
                    `
                } else {
                    message.classList.add('message_error');
                    message.innerHTML = `
                        Ошибка
                    `
                }

                articleRatesFormDOM.append(message);

                setTimeout(() => {
                    message.remove();
                }, 2000)
            });
        });

        console.log(questionsArr);
    };
});