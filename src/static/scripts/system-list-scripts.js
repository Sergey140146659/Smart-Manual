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


//    Load System Table

    loadSystemTable = async function () {
        response = await getResponse("/system/get_all_systems");
        systemsList = response["data"];

        const table = document.querySelector(".systems-list-body");

        systemsList.forEach(item => {
            const newTr = document.createElement("tr");
            newTr.classList.add("systems-list__item");
            newTr.innerHTML = `
                <th class="system_id">${item.id}</th>
                <th class="system_name">${item.name}</th>
                <th class="system_token">${item.token}</th>
                <th class="system_region">${item.region}</th>
                <th class="system_type">${item.system_type}</th>
                <th class="system_bug_tracker">${item.bug_tracker}</th>
                <th class="system_delete">
                    <button class="system_delete_button" type="button">Удалить</button>
                </th>
            `;

            const deleteSystemButton = newTr.querySelector('.system_delete_button');
            deleteSystemButton.addEventListener('click', () => {
                deleteSystem(item.id).then(data => {
                    table.innerHTML = '';
                    loadSystemTable();
                });
            });

            table.append(newTr);
        });
    }

    loadSystemTable();


//    Clear System Table

    const systemTable = document.querySelector('.systems-list-body');

    let clearSystemTable = function() {
        systemTable.innerHTML = ``;
    }


//    Add System Modal Window

    const openButton = document.querySelector('.add_system_button');
    const modal = document.querySelector('.modal');
    const closeModalElements = document.querySelectorAll('.close-modal-area');
    const addSystemForm = document.querySelector('#add_system_form');

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

    addSystemForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const addSystemFormData = new FormData(addSystemForm);
        let sendData = {};
        addSystemFormData.forEach((value, key) => sendData[key] = value);
        let json = JSON.stringify(sendData);
        postRequest('/system/add_system', json)
            .then(data => {
                clearSystemTable();
                 loadSystemTable();
                 modal.classList.add('hidden');
            });
    });

//    Delete System

    async function deleteSystem(systemId) {
        const res = await fetch(`/system/delete_system/${systemId}`, {
            method: "DELETE",
            headers: {
                'Content-type': 'application/json'
            },
            body: {"system_id": systemId}
        });

        return await res;
    }
});
