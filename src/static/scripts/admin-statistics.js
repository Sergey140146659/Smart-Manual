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

//  Set current date

    const setCurrentDate = function () {
        const startDateDOM = document.querySelector("#date_start");
        const endDateDOM = document.querySelector("#date_end");

        const currentDate = new Date();
        currentDate.setHours(3, 0, 0, 0);
        startDateDOM.value = currentDate.toISOString().slice(0,16);

        currentDate.setHours(27, 0, 0, 0);
        endDateDOM.value = currentDate.toISOString().slice(0,16);
    };

    setCurrentDate();


//  Send form

    sendDateForm = async function (systemId) {
        const startDate = document.querySelector("#date_start").value;
        const endDate = document.querySelector("#date_end").value;
        const url = `/query/get_queries_stats?system_id=${systemId}&date_start=${startDate}&date_end=${endDate}`;

        let response = await getResponse(url);
        return response;
    }


//    Load System Table

    loadSystemTable = async function () {
        const table = document.querySelector(".systems-list-body");
        table.innerHTML = '';

        response = await getResponse("/system/get_all_systems");
        systemsList = response["data"];

        const startDate = document.querySelector("#date_start").value;
        const endDate = document.querySelector("#date_end").value;

        let allSystemCounter = 0;
        for (const item of systemsList) {
            const newTr = document.createElement("tr");
            const curSystemCounter = await sendDateForm(item.id);

            if (curSystemCounter.status == "error") {
                curSystemCounter.data = 0;
            }

            allSystemCounter += curSystemCounter.data;

            newTr.classList.add("systems-list__item");
            newTr.innerHTML = `
                <th class="system_id">${item.id}</th>
                <th class="system_name">${item.name}</th>
                <th class="system_requests_count">
                    <a class="" href="/pages/admin_queries?system_id=${item.id}&date_start=${startDate}&date_end=${endDate}" target="_blank">${curSystemCounter.data}</a>
                </th>
            `;
            table.append(newTr);
        }

        console.log(allSystemCounter);
        const newTr = document.createElement("tr");
        newTr.classList.add("systems-list__item");
        newTr.innerHTML = `
            <th class="system_id"></th>
            <th class="system_name">Всего</th>
            <th class="system_requests_count">
                <a class="" href="/pages/admin_queries" target="_blank">${allSystemCounter}</a>
            </th>
        `;
        table.append(newTr);
    }

    loadSystemTable();

    const dateFormDOM = document.querySelector(".date_range")
    dateFormDOM.addEventListener('submit', (e) => {
        e.preventDefault();
        loadSystemTable();
    });
});

