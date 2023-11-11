window.addEventListener('DOMContentLoaded', () => {

//    Post Request

    const postRequest = async (url, data = "") => {
        const res = await fetch(url, {
            method: "POST",
            headers: {
                'Content-type': 'application/json'
            },
            body: data
        });

        return await res.json();
    }


//    Get Response

    const getResponse = async (url) => {
        const response = await fetch(url, {
            method: 'GET'
        });
        return response.json();
    }


//    Load Users Table

    loadUserTable = async function () {
        response = await getResponse("/user/get_all_users");
        usersList = response["data"];

        const table = document.querySelector(".users-list-body");
        table.innerHTML = '';

        usersList.forEach(user => {
            let item = user['User'];
            let newTr = document.createElement("tr");

            newTr.classList.add("systems-list__item");
            newTr.innerHTML = `
                <th class="user_id">${item.id}</th>
                <th class="user_email">${item.email}</th>
                <th class="user_username">${item.username}</th>
                <th class="user_is_superuser">${item.is_superuser}</th>
            `

            const changeTh = document.createElement('th');
            changeTh.classList.add('user_change');
            changeTh.innerHTML = `
                <button class="admin_users_change_button" type="button">Изменить</button>
            `;

            const changeButton = changeTh.querySelector('button');


            const deleteTh = document.createElement('th');
            deleteTh.classList.add('user_delete');
            deleteTh.innerHTML = `
                <button class="admin_users_delete_button" type="button">Удалить</button>
            `;

            const deleteButton = deleteTh.querySelector('button');
            deleteButton.addEventListener('click', () => {
                deleteUser(item.id)
                    .then(data => {
                        loadUserTable();
                    });
            });

            newTr.append(changeTh);
            newTr.append(deleteTh);

            table.append(newTr);
        });
    }

    loadUserTable();


//    Delete User

    async function deleteUser(userId) {
        const res = await fetch(`/user/delete_user/${userId}`, {
            method: "DELETE",
            headers: {
                'Content-type': 'application/json'
            },
            body: {"user_id": userId}
        });

        return await res;
    }


//   Add User Modal Window

    function addUser () {
        const openButton = document.querySelector('.add_user_button');
        const modal = document.querySelector('.add_user_modal');
        const closeModalElements = document.querySelectorAll('.close-modal-area');
        const addUserForm = document.querySelector('#add_user_form');

        openButton.addEventListener('click', () => {
            modal.classList.remove('hidden');
        });

        closeModalElements.forEach(item => {
            item.addEventListener('click', (e) => {
                if (e.target.classList.contains('close-modal-area')) {
                    modal.classList.add('hidden');
                }
            });
        });

        addUserForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const addUserFormData = new FormData(addUserForm);
            let sendData = {};
            addUserFormData.forEach((value, key) => sendData[key] = value);
            console.log(sendData);
            let json = JSON.stringify(sendData);
            console.log(json);
            postRequest('/user/create_user', json)
                .then(data => {
                     loadUserTable();
                     modal.classList.add('hidden');
                });
        });
    }

    addUser();
});